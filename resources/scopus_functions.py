import json
import pandas as pd
import logging
import os

from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch


# Read environment variables
exec(open("env_variables.py").read())
module_logger = logging.getLogger("main.resources.scopus_functions")


def get_environment_var(env, fallback):
    """
    Get environment variable or fallback value.
    """
    try:
        var = os.environ[env]
        if isinstance(fallback, int):
            var = int(var)
    except (KeyError, ValueError):
        if fallback is None:
            module_logger.error(
                f"The required environment variable '{env}' is not set \
                    and has not got a fallback value.")
            raise
        else:
            var = fallback
    return var


project_dir = get_environment_var("project_dir", None)
scopus_config_file = get_environment_var("scopus_config_file", None)
scopus_data_dir = get_environment_var("scopus_data_dir", None)

# Read Scopus API key
con_file = open(scopus_config_file)
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
columns_to_hide = [
    "openaccess",
]


# Functions to retrieve results from Scopus API
def retrieve_results_from_query(query: str) -> pd.DataFrame:
    """
    Retrieve results from query.
    """
    module_logger.info(
        f"Retrieving results from Scopus API for query: {query}")
    # Initialize document search object and execute search
    doc_srch = ElsSearch(query, "scopus")
    doc_srch.execute(client, get_all=True)
    # Retrieve results
    results = doc_srch.results
    module_logger.info(f"{len(results)} results retrieved from Scopus API.")
    results_df = convert_results_to_dataframe(results)
    module_logger.info("Query results converted to dataframe.")
    return results_df


def retrieve_results_from_list_of_queries(
    list_of_queries: list[str],
    max_date: str,
) -> pd.DataFrame:
    """
    Retrieve results from list of queries and concatenate them.
    """
    module_logger.info(
        f"Retrieving results from {len(list_of_queries)} queries.")
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
    module_logger.info(
        f"{len(results_df)} results retrieved from the list of queries.")
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
        module_logger.info(
            f"Columns not converted to dataframe: {results_df.columns})")
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
    - convert openaccess column to boolean
    """
    module_logger.info("Applying further transformations to dataframe.")
    df_copy = df.copy()
    if max_date:
        module_logger.info(f"Filtering by max_date: {max_date}")
        df_copy = df_copy[df_copy["prism:coverDate"] < max_date]
        module_logger.info(
            f"{len(df_copy)} results after filtering by max_date.")
    df_copy.drop_duplicates(subset=["dc:identifier"], inplace=True)
    module_logger.info(f"{len(df_copy)} results after deduplication.")
    df_copy.reset_index(drop=True, inplace=True)
    df_copy["openaccess"] = df_copy["openaccess"].astype(bool)
    module_logger.info("Further transformations applied to dataframe.")
    return df_copy
