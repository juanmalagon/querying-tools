from unittest.mock import patch

import pandas as pd

from resources.querying_tools import (
    create_localized_queries,
    determine_localization_in_title,
    find_localization_in_text,
    language_bias_tool,
    localization_bias_tool,
    publication_bias_tool,
    remove_accents_and_special_chars,
    scopus_query_list_constructor,
)

# --- language_bias_tool ---


def test_language_bias_tool_removes_language_filter():
    query = "ALL({education}) AND LANGUAGE(english) AND SRCTYPE(j)"

    result = language_bias_tool(query)

    assert "LANGUAGE(english)" not in result
    assert "SRCTYPE(j)" in result


def test_language_bias_tool_no_language_filter_is_unchanged():
    query = "ALL({education}) AND SRCTYPE(j)"

    result = language_bias_tool(query)

    assert result == query


def test_language_bias_tool_empty_string():
    result = language_bias_tool("")

    assert result == ""


# --- publication_bias_tool ---


def test_publication_bias_tool_removes_source_type_filter():
    query = "ALL({education}) AND LANGUAGE(english) AND SRCTYPE(j)"

    result = publication_bias_tool(query)

    assert "SRCTYPE(j)" not in result
    assert "LANGUAGE(english)" in result


def test_publication_bias_tool_no_source_filter_is_unchanged():
    query = "ALL({education}) AND LANGUAGE(english)"

    result = publication_bias_tool(query)

    assert result == query


def test_publication_bias_tool_empty_string():
    result = publication_bias_tool("")

    assert result == ""


# --- remove_accents_and_special_chars ---


def test_remove_accents_handles_accented_characters():
    result = remove_accents_and_special_chars("éxité")

    assert result == "exite"


def test_remove_accents_handles_apostrophes():
    result = remove_accents_and_special_chars("Côte d'Ivoire")

    assert "Cote" in result
    assert "Ivoire" in result


def test_remove_accents_strips_special_characters():
    result = remove_accents_and_special_chars("hello! world?")

    assert result == "hello world"


# --- find_localization_in_text ---


def test_find_localization_in_text_detects_country():
    text = "Education policy in Belgium and France"

    assert find_localization_in_text(text) is True


def test_find_localization_in_text_no_match():
    text = "A theoretical model of efficiency"

    assert find_localization_in_text(text) is False


def test_find_localization_in_text_with_custom_location_list():
    text = "Results from Mars academy"

    result = find_localization_in_text(
        text,
        list_of_locations=["mars"],
    )

    assert result is True


# --- determine_localization_in_title ---


def test_determine_localization_in_title_adds_column():
    df = pd.DataFrame({"dc:title": ["Study in Belgium", "Generic theory"]})
    result = determine_localization_in_title(df)

    assert "localization_in_title" in result.columns
    assert result["localization_in_title"].tolist() == [True, False]


# --- scopus_query_list_constructor ---


def test_scopus_query_list_constructor_splits_long_list():
    initial = "ALL({education})"
    terms = [f"term{i}" for i in range(50)]

    result = scopus_query_list_constructor(
        initial_query=initial,
        long_list=terms,
        search_field="TITLE-ABS-KEY",
        step=20,
    )

    assert len(result) == 3
    assert all(q.startswith(initial) for q in result)
    assert all("TITLE-ABS-KEY" in q for q in result)


def test_scopus_query_list_constructor_single_query_when_under_step():
    initial = "ALL({education})"
    terms = ["a", "b", "c"]

    result = scopus_query_list_constructor(
        initial_query=initial,
        long_list=terms,
        step=20,
    )

    assert len(result) == 1
    assert result[0].startswith(initial)


# --- create_localized_queries ---


def test_create_localized_queries_produces_disjoint_sets():
    """Weird + complement should cover the entire universe exactly once."""
    universe = ["zzalpha", "zzbeta", "zzgamma", "zzdelta"]
    weird = ["zzalpha", "zzbeta"]

    result = create_localized_queries(
        original_query="ALL({xquery})",
        list_of_country_identifiers=weird,
        universe=universe,
        nr_identifiers_per_query=10,
    )

    localized = result["localized_queries"]
    complement = result["localized_queries_complement"]

    assert len(localized) == 1
    assert len(complement) == 1
    assert "zzalpha" in localized[0]
    assert "zzbeta" in localized[0]
    assert "zzgamma" in complement[0]
    assert "zzdelta" in complement[0]
    assert "zzalpha" not in complement[0]
    assert "zzgamma" not in localized[0]


# --- localization_bias_tool ---


def _make_mock_record(
    identifier: str,
    title: str,
    cover_date: str = "2023-01-01",
) -> dict:
    """Helper to create a minimal valid Scopus record dict."""
    return {
        "dc:identifier": identifier,
        "dc:title": title,
        "dc:creator": "Author",
        "prism:publicationName": "Journal",
        "prism:coverDate": cover_date,
        "prism:aggregationType": "Journal",
        "subtypeDescription": "Article",
        "prism:doi": f"10.1000/{identifier}",
        "eid": f"eid_{identifier}",
        "openaccess": 1,
    }


def test_localization_bias_tool_labels_weird_and_no_weird():
    """Records retrieved via weird/universe queries should be labelled correctly."""
    weird_records = [
        _make_mock_record("id_weird", "Study in Belgium"),
    ]
    complement_records = [
        _make_mock_record("id_no_weird", "Study in Chile"),
    ]

    with patch(
        "resources.querying_tools.retrieve_results_from_list_of_queries"
    ) as mock_retrieve:
        mock_retrieve.side_effect = [
            pd.DataFrame(weird_records),
            pd.DataFrame(complement_records),
        ]

        result = localization_bias_tool(
            query="ALL({education})",
            max_date="2025-01-01",
            list_of_country_identifiers=["belgium"],
        )

    assert "localized_weird" in result.columns
    assert "localized_no_weird" in result.columns
    assert "localization_in_title" in result.columns

    assert result.loc[result["dc:identifier"] == "id_weird", "localized_weird"].iloc[0]
    assert not result.loc[
        result["dc:identifier"] == "id_weird", "localized_no_weird"
    ].iloc[0]

    assert not result.loc[
        result["dc:identifier"] == "id_no_weird", "localized_weird"
    ].iloc[0]
    assert result.loc[
        result["dc:identifier"] == "id_no_weird", "localized_no_weird"
    ].iloc[0]


def test_localization_bias_tool_deduplicates_overlap():
    """A record appearing in both weird and complement should be deduplicated."""
    shared = _make_mock_record("id_shared", "Study in Shared")

    with patch(
        "resources.querying_tools.retrieve_results_from_list_of_queries"
    ) as mock_retrieve:
        mock_retrieve.side_effect = [
            pd.DataFrame([shared]),
            pd.DataFrame([shared]),
        ]

        result = localization_bias_tool(
            query="ALL({education})",
            max_date="2025-01-01",
            list_of_country_identifiers=["belgium"],
        )

    assert len(result) == 1
    assert result["localized_weird"].iloc[0]
    assert result["localized_no_weird"].iloc[0]


def test_localization_bias_tool_detects_localization_in_title():
    """Title containing a country name should be flagged as localized."""
    record_with_country = _make_mock_record("id_1", "Education in France: an analysis")
    record_without = _make_mock_record("id_2", "A theoretical approach")

    with patch(
        "resources.querying_tools.retrieve_results_from_list_of_queries"
    ) as mock_retrieve:
        mock_retrieve.side_effect = [
            pd.DataFrame([record_with_country]),
            pd.DataFrame([record_without]),
        ]

        result = localization_bias_tool(
            query="ALL({education})",
            max_date="2025-01-01",
            list_of_country_identifiers=["belgium"],
        )

    assert result.loc[result["dc:identifier"] == "id_1", "localization_in_title"].iloc[
        0
    ]
    assert not result.loc[
        result["dc:identifier"] == "id_2", "localization_in_title"
    ].iloc[0]


def test_localization_bias_tool_empty_results():
    """Should return an empty DataFrame cleanly when no results."""
    with patch(
        "resources.querying_tools.retrieve_results_from_list_of_queries"
    ) as mock_retrieve:
        mock_retrieve.return_value = pd.DataFrame(
            columns=[
                "dc:identifier",
                "dc:title",
                "dc:creator",
                "prism:publicationName",
                "prism:coverDate",
                "prism:aggregationType",
                "subtypeDescription",
                "prism:doi",
                "eid",
                "openaccess",
            ]
        )

        result = localization_bias_tool(
            query="ALL({no_results})",
            max_date="2025-01-01",
            list_of_country_identifiers=["belgium"],
        )

    assert len(result) == 0
    assert "localized_weird" in result.columns
    assert "localized_no_weird" in result.columns
    assert "localization_in_title" in result.columns
