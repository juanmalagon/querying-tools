import pandas as pd

from resources.scopus_functions import (
    apply_further_transformations,
    convert_results_to_dataframe,
    selected_columns,
)

# --- convert_results_to_dataframe ---


def test_convert_results_to_dataframe_extracts_selected_columns():
    records = [
        {
            "dc:identifier": "SCOPUS_ID:1",
            "dc:title": "Title A",
            "dc:creator": "Doe",
            "prism:publicationName": "Journal X",
            "prism:coverDate": "2023-01-01",
            "prism:aggregationType": "Journal",
            "subtypeDescription": "Article",
            "prism:doi": "10.1000/1",
            "eid": "eid1",
            "openaccess": 1,
            "extra_field": "should be dropped",
        },
    ]

    result = convert_results_to_dataframe(records)

    assert list(result.columns) == selected_columns
    assert "extra_field" not in result.columns
    assert len(result) == 1
    assert result["dc:identifier"].iloc[0] == "SCOPUS_ID:1"


def test_convert_results_to_dataframe_deduplicates():
    records = [
        {
            "dc:identifier": "SCOPUS_ID:1",
            "dc:title": "Title A",
            "dc:creator": "Doe",
            "prism:publicationName": "Journal X",
            "prism:coverDate": "2023-01-01",
            "prism:aggregationType": "Journal",
            "subtypeDescription": "Article",
            "prism:doi": "10.1000/1",
            "eid": "eid1",
            "openaccess": 1,
        },
        {
            "dc:identifier": "SCOPUS_ID:1",  # duplicate
            "dc:title": "Title A",
            "dc:creator": "Doe",
            "prism:publicationName": "Journal X",
            "prism:coverDate": "2023-01-01",
            "prism:aggregationType": "Journal",
            "subtypeDescription": "Article",
            "prism:doi": "10.1000/1",
            "eid": "eid1",
            "openaccess": 1,
        },
    ]

    result = convert_results_to_dataframe(records)

    assert len(result) == 1


def test_convert_results_to_dataframe_casts_openaccess_to_int():
    records = [
        {
            "dc:identifier": "SCOPUS_ID:1",
            "dc:title": "Title A",
            "dc:creator": "Doe",
            "prism:publicationName": "Journal X",
            "prism:coverDate": "2023-01-01",
            "prism:aggregationType": "Journal",
            "subtypeDescription": "Article",
            "prism:doi": "10.1000/1",
            "eid": "eid1",
            "openaccess": "1",
        },
    ]

    result = convert_results_to_dataframe(records)

    assert result["openaccess"].dtype == "int64"
    assert result["openaccess"].iloc[0] == 1


def test_convert_results_to_dataframe_missing_columns_returns_empty():
    records = [{"unexpected_column": "value"}]

    result = convert_results_to_dataframe(records)

    assert list(result.columns) == selected_columns
    assert len(result) == 0


def test_convert_results_to_dataframe_empty_list():
    result = convert_results_to_dataframe([])

    assert list(result.columns) == selected_columns
    assert len(result) == 0


# --- apply_further_transformations ---


def test_apply_further_transformations_filters_by_max_date():
    df = pd.DataFrame(
        {
            "dc:identifier": ["id1", "id2", "id3"],
            "prism:coverDate": ["2020-01-01", "2022-06-15", "2024-12-31"],
            "openaccess": [1, 0, 1],
        },
    )

    result = apply_further_transformations(df, max_date="2023-01-01")

    # Only records with coverDate < "2023-01-01" should remain
    assert len(result) == 2
    assert set(result["dc:identifier"]) == {"id1", "id2"}


def test_apply_further_transformations_no_max_date_keeps_all():
    df = pd.DataFrame(
        {
            "dc:identifier": ["id1", "id2"],
            "prism:coverDate": ["2020-01-01", "2024-12-31"],
            "openaccess": [1, 0],
        },
    )

    result = apply_further_transformations(df)

    assert len(result) == 2


def test_apply_further_transformations_deduplicates():
    df = pd.DataFrame(
        {
            "dc:identifier": ["id1", "id1", "id2"],
            "prism:coverDate": ["2020-01-01", "2020-01-01", "2020-01-01"],
            "openaccess": [1, 1, 0],
        },
    )

    result = apply_further_transformations(df)

    assert len(result) == 2
    assert result.index.is_monotonic_increasing


def test_apply_further_transformations_casts_openaccess_to_bool():
    df = pd.DataFrame(
        {
            "dc:identifier": ["id1"],
            "prism:coverDate": ["2020-01-01"],
            "openaccess": [1],
        },
    )

    result = apply_further_transformations(df)

    assert result["openaccess"].dtype == "bool"
    assert bool(result["openaccess"].iloc[0]) is True


def test_apply_further_transformations_does_not_mutate_original():
    df = pd.DataFrame(
        {
            "dc:identifier": ["id1", "id2"],
            "prism:coverDate": ["2020-01-01", "2020-01-01"],
            "openaccess": [1, 0],
        },
    )

    apply_further_transformations(df)

    # Original should be unchanged
    assert len(df) == 2
    assert df["openaccess"].dtype == "int64"
