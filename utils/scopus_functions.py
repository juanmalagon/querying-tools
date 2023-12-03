import logging
import pandas as pd
import json

# import re

from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch

from utils import handler as h
from utils import query_helpers as qh

# from utils import country_lists as cl


# Load configuration
module_logger = logging.getLogger("main.utils.scopus_functions")
pd.options.display.max_columns = None
con_file = open(h.scopus_config_file)
config = json.load(con_file)
con_file.close()

# Initialize Elsevier client
client = ElsClient(config["apikey"])

# Define selected columns
selected_columns = [
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


# Functions to retrieve results from Scopus API
def scopus_query_list_constructor(
    initial_query: str, long_list: list[str], search_field: str = "ALL", step: int = 20
):
    """
    Constructs a list of queries for the Scopus Search API. This process
    is necessary because the Scopus Search API only allows queries with
    limited length. We use it to construct a list of queries that will
    look for country names and demonyms in search fields.
    - The initial_query is a string that will be used as the first part of
    each query.
    - The long_list is a list of strings that will be used as the
    second part of each query.
    - The search_field is the field in which the second part of the query
    will be searched.
    - The step is the number of elements of the long list that will be
    included in each query.
    """
    list_of_queries = []
    for i in range(0, len(long_list), step):
        list_of_queries.append(
            initial_query
            + " AND "
            + search_field
            + "({"
            + "} OR {".join(long_list[i : i + step])
            + "})"
        )
    return list_of_queries


def retrieve_results_from_query(query: str) -> pd.DataFrame:
    """
    Retrieve results from query.
    """
    module_logger.info(f"Retrieving results from Scopus API for query: {query}")
    # Initialize document search object and execute search
    doc_srch = ElsSearch(query, "scopus")
    doc_srch.execute(client, get_all=True)
    # Retrieve results
    results = doc_srch.results
    module_logger.info(f"{len(results)} results retrieved from Scopus API.")

    results_df = convert_results_to_dataframe(results)
    if len(results_df) > 0:
        results_df["localization_in_title_abstract_or_key"] = "TITLE-ABS-KEY" in query
    else:
        results_df["localization_in_title_abstract_or_key"] = None
    module_logger.info("Query results converted to dataframe.")
    return results_df


def retrieve_results_from_list_of_queries(
    list_of_queries: list[str],
    max_date: str,
) -> pd.DataFrame:
    """
    Retrieve results from list of queries and concatenate them.
    """
    module_logger.info(f"Retrieving results from {len(list_of_queries)} queries.")
    results_dfs = []
    for query in list_of_queries:
        results_df = retrieve_results_from_query(query)
        results_dfs.append(results_df)
    module_logger.info(f"Concatenating {len(results_dfs)} dataframes.")
    results_df = pd.concat(results_dfs)
    results_df = results_df.drop_duplicates(subset=["dc:identifier"])
    results_df = results_df.reset_index(drop=True)
    module_logger.info(
        f"Deduplicated results in concatenated dataframe: {len(results_df)}"
    )
    results_df = apply_further_transformations(results_df, max_date=max_date)
    module_logger.info(f"{len(results_df)} results retrieved from the list of queries.")
    return results_df


# Functions to process imported results
def convert_results_to_dataframe(
    results: list, selected_columns=selected_columns
) -> pd.DataFrame:
    """Convert results to dataframe."""
    module_logger.info(f"Converting {len(results)} results to dataframe.")
    results_df = pd.DataFrame.from_records(results)
    try:
        results_df = results_df[selected_columns]
        results_df = results_df.drop_duplicates(subset=["dc:identifier"])
        results_df["openaccess"] = results_df["openaccess"].astype(int)
        results_df = results_df.reset_index(drop=True)
        module_logger.info(
            f"Deduplicated results stored in dataframe: {len(results_df)}"
        )
    except KeyError:
        module_logger.info(f"Columns not converted to dataframe: {results_df.columns})")
        results_df = pd.DataFrame(columns=selected_columns)
    module_logger.info(f"{len(results_df)} results converted to dataframe.")
    return results_df


def apply_further_transformations(
    df: pd.DataFrame,
    max_date: str = None,
) -> pd.DataFrame:
    """
    Apply further transformations to dataframe:
    - add column 'localization_in_title' (boolean)
    - filter by max_date
    - drop duplicates
    - reset index
    """
    module_logger.info("Applying further transformations to dataframe.")
    df_copy = df.copy()
    df_copy = qh.determine_localization_in_title(df_copy)
    if max_date:
        module_logger.info(f"Filtering by max_date: {max_date}")
        df_copy = df_copy[df_copy["prism:coverDate"] < max_date]
        module_logger.info(f"{len(df_copy)} results after filtering by max_date.")
    df_copy.drop_duplicates(subset=["dc:identifier"], inplace=True)
    module_logger.info(f"{len(df_copy)} results after deduplication.")
    df_copy.reset_index(drop=True, inplace=True)
    module_logger.info("Further transformations applied to dataframe.")
    return df_copy


# Functions to export results to csv
def export_to_csv(df: pd.DataFrame, file_name: str) -> None:
    """Export dataframe to csv."""
    module_logger.info(f"Exporting dataframe to csv: {file_name}")
    file_name_extended = file_name + "-" + h.run_date + "-" + h.run_serial
    df["run_date"] = h.run_date
    df["run_serial"] = h.run_serial
    df.to_csv(
        path_or_buf=h.scopus_data_dir + file_name_extended + ".csv",
        sep=",",
        index=False,
        encoding="utf-8",
    )
    module_logger.info(f"Dataframe exported to csv: {file_name_extended}")
    return None
