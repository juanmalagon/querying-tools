from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from resources.scopus_functions import (
    get_client,
    retrieve_results_from_list_of_queries,
    retrieve_results_from_query,
)

# --- get_client ---


def test_get_client_initializes_once():
    """get_client should reuse the same client after first call."""
    with patch("resources.scopus_functions.ElsClient") as mock_els_client_class:
        mock_client_instance = MagicMock()
        mock_els_client_class.return_value = mock_client_instance

        # Patch the settings.resolve_scopus_api_key to avoid RuntimeError
        import resources.scopus_functions as sf

        sf.client = None

        with patch.object(
            sf.settings.__class__, "resolve_scopus_api_key", return_value="fake-key"
        ):
            client1 = get_client()
            client2 = get_client()

        # ElsClient constructor should be called exactly once
        mock_els_client_class.assert_called_once()
        assert client1 is client2 is mock_client_instance


def test_get_client_passes_api_key():
    """get_client should pass the resolved API key to ElsClient."""
    import resources.scopus_functions as sf

    with patch("resources.scopus_functions.ElsClient") as mock_els_client_class:
        sf.client = None

        with patch.object(
            sf.settings.__class__, "resolve_scopus_api_key", return_value="test-api-key"
        ):
            get_client()

        mock_els_client_class.assert_called_once_with("test-api-key")


# --- retrieve_results_from_query ---


def test_retrieve_results_from_query_basic():
    """Should return a DataFrame with results from the Scopus API."""
    mock_results = [
        {
            "dc:identifier": "SCOPUS_ID:1",
            "dc:title": "Test Title",
            "dc:creator": "Author",
            "prism:publicationName": "Journal",
            "prism:coverDate": "2023-01-01",
            "prism:aggregationType": "Journal",
            "subtypeDescription": "Article",
            "prism:doi": "10.1000/1",
            "eid": "eid1",
            "openaccess": 1,
        },
    ]

    with patch("resources.scopus_functions.ElsSearch") as mock_els_search_class:
        mock_search = MagicMock()
        mock_search.results = mock_results
        mock_els_search_class.return_value = mock_search

        with patch("resources.scopus_functions.get_client") as mock_get_client:
            mock_get_client.return_value = MagicMock()

            result = retrieve_results_from_query("ALL({test})")

            mock_els_search_class.assert_called_once_with("ALL({test})", "scopus")
            mock_search.execute.assert_called_once_with(
                mock_get_client.return_value, get_all=True
            )
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 1
            assert result["dc:identifier"].iloc[0] == "SCOPUS_ID:1"


def test_retrieve_results_from_query_empty_results():
    """Should handle empty results from the API."""
    with patch("resources.scopus_functions.ElsSearch") as mock_els_search_class:
        mock_search = MagicMock()
        mock_search.results = []
        mock_els_search_class.return_value = mock_search

        with patch("resources.scopus_functions.get_client"):
            result = retrieve_results_from_query("ALL({nothing})")

            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0


def test_retrieve_results_from_query_multiple_records():
    """Should correctly handle multiple records from the API."""
    mock_results = [
        {
            "dc:identifier": f"SCOPUS_ID:{i}",
            "dc:title": f"Title {i}",
            "dc:creator": f"Author {i}",
            "prism:publicationName": f"Journal {i}",
            "prism:coverDate": f"2023-01-{i:02d}",
            "prism:aggregationType": "Journal",
            "subtypeDescription": "Article",
            "prism:doi": f"10.1000/{i}",
            "eid": f"eid{i}",
            "openaccess": i % 2,
        }
        for i in range(1, 6)
    ]

    with patch("resources.scopus_functions.ElsSearch") as mock_els_search_class:
        mock_search = MagicMock()
        mock_search.results = mock_results
        mock_els_search_class.return_value = mock_search

        with patch("resources.scopus_functions.get_client"):
            result = retrieve_results_from_query("ALL({multi})")

            assert len(result) == 5
            assert list(result["dc:identifier"]) == [
                f"SCOPUS_ID:{i}" for i in range(1, 6)
            ]


# --- retrieve_results_from_list_of_queries ---


def make_mock_result(identifier_suffix: str) -> list[dict]:
    """Helper to create a minimal valid result dict."""
    return [
        {
            "dc:identifier": f"SCOPUS_ID:{identifier_suffix}",
            "dc:title": f"Title {identifier_suffix}",
            "dc:creator": "Author",
            "prism:publicationName": "Journal",
            "prism:coverDate": "2023-01-01",
            "prism:aggregationType": "Journal",
            "subtypeDescription": "Article",
            "prism:doi": f"10.1000/{identifier_suffix}",
            "eid": f"eid_{identifier_suffix}",
            "openaccess": 1,
        },
    ]


def test_retrieve_results_from_list_of_queries_concatenates():
    """Should retrieve results for each query and concatenate them."""
    with patch(
        "resources.scopus_functions.retrieve_results_from_query"
    ) as mock_retrieve:
        mock_retrieve.side_effect = [
            pd.DataFrame(make_mock_result("q1")),
            pd.DataFrame(make_mock_result("q2")),
            pd.DataFrame(make_mock_result("q3")),
        ]

        result = retrieve_results_from_list_of_queries(
            ["query1", "query2", "query3"],
            max_date="2024-01-01",
        )

        assert len(result) == 3
        assert mock_retrieve.call_count == 3


def test_retrieve_results_from_list_of_queries_deduplicates():
    """Should remove duplicate dc:identifiers across queries."""
    duplicate_record = {
        "dc:identifier": "SCOPUS_ID:dup",
        "dc:title": "Duplicate Title",
        "dc:creator": "Author",
        "prism:publicationName": "Journal",
        "prism:coverDate": "2023-01-01",
        "prism:aggregationType": "Journal",
        "subtypeDescription": "Article",
        "prism:doi": "10.1000/dup",
        "eid": "eid_dup",
        "openaccess": 1,
    }

    with patch(
        "resources.scopus_functions.retrieve_results_from_query"
    ) as mock_retrieve:
        mock_retrieve.side_effect = [
            pd.DataFrame([duplicate_record]),
            pd.DataFrame([duplicate_record]),
        ]

        result = retrieve_results_from_list_of_queries(
            ["query1", "query2"],
            max_date="2024-01-01",
        )

        assert len(result) == 1
        assert result["dc:identifier"].iloc[0] == "SCOPUS_ID:dup"


def test_retrieve_results_from_list_of_queries_applies_max_date():
    """Should apply the max_date filter to the final result."""
    record_before = {
        "dc:identifier": "SCOPUS_ID:old",
        "dc:title": "Old Title",
        "dc:creator": "Author",
        "prism:publicationName": "Journal",
        "prism:coverDate": "2020-01-01",
        "prism:aggregationType": "Journal",
        "subtypeDescription": "Article",
        "prism:doi": "10.1000/old",
        "eid": "eid_old",
        "openaccess": 1,
    }
    record_after = {
        "dc:identifier": "SCOPUS_ID:new",
        "dc:title": "New Title",
        "dc:creator": "Author",
        "prism:publicationName": "Journal",
        "prism:coverDate": "2025-06-01",
        "prism:aggregationType": "Journal",
        "subtypeDescription": "Article",
        "prism:doi": "10.1000/new",
        "eid": "eid_new",
        "openaccess": 1,
    }

    with patch(
        "resources.scopus_functions.retrieve_results_from_query"
    ) as mock_retrieve:
        mock_retrieve.return_value = pd.DataFrame([record_before, record_after])

        result = retrieve_results_from_list_of_queries(
            ["query1"],
            max_date="2025-01-01",
        )

        assert len(result) == 1
        assert result["dc:identifier"].iloc[0] == "SCOPUS_ID:old"


def test_retrieve_results_from_list_of_queries_empty_list_raises():
    """Empty query list leads to pd.concat on no DataFrames."""
    with (
        patch("resources.scopus_functions.retrieve_results_from_query"),
        pytest.raises(ValueError, match="No objects to concatenate"),
    ):
        retrieve_results_from_list_of_queries(
            [],
            max_date="2024-01-01",
        )
