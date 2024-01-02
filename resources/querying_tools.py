import re
import unicodedata
import pandas as pd
from resources.scopus_functions import retrieve_results_from_list_of_queries
from resources.country_lists import (
    countries,
    demonyms,
    continents_names,
    continents_demonyms,
    weird_countries,
    weird_demonyms,
)


# Language bias tool
def language_bias_tool(query: str) -> str:
    """
    Returns a query without the language restriction.
    """
    return re.sub(r"(AND\s)*LANGUAGE\(\w+\)", "", query)


# Publication bias tool
def publication_bias_tool(query: str) -> str:
    """
    Returns a query without the source type restriction.
    """
    return re.sub(r"(AND\s)*SRCTYPE\(\w+\)", "", query)


# Helper functions for localization bias tool
def remove_accents_and_special_chars(text):
    """
    Removes accents and special characters from text.
    """
    text = ''.join(char for char in unicodedata.normalize('NFD', text)
                   if unicodedata.category(char) != 'Mn')
    text = text.replace("'", " ")
    # text = re.sub(r'\'', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text


def find_localization_in_text(
    text: str,
    list_of_locations: list[str] =
        countries+demonyms+continents_names+continents_demonyms,
) -> bool:
    """
    Returns True if any country name or demonym is found in the text.
    """
    text = remove_accents_and_special_chars(text)
    text_words = text.lower().split()
    if any(location.lower() in text_words for location in list_of_locations):
        return True
    else:
        return False


def determine_localization_in_title(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add column 'localization_in_title' (boolean)
    """
    df_copy = df.copy()
    df_copy["localization_in_title"] = df["dc:title"].apply(
        find_localization_in_text)
    return df_copy


def scopus_query_list_constructor(
    initial_query: str,
    long_list: list[str],
    search_field: str = "ALL",
    step: int = 20
):
    """
    Constructs a list of queries for the Scopus Search API adding all the
    keywords in the long_list to the initial_query.
    This process is necessary because the Scopus Search API limits the lenght
    of the query strings it accepts.
    Hence, if we need to look for many terms within a field (e.g., when
    looking for many possible country names and demonyms in the title, abstract
    or keywords field) we need to split the list of terms into smaller sublists
    and construct a single query for each sublist.

    - initial_query is a fixed string that will be used as the first part of
    each query.
    - long_list is a list of strings that will be used as the second part of
    each query.
    - search_field is the field in which the second part of the query will be
    searched.
    - step is the number of elements of the long list that will be included in
    each query.
    """
    list_of_queries = []
    for i in range(0, len(long_list), step):
        list_of_queries.append(
            initial_query
            + " AND "
            + search_field
            + "({"
            + "} OR {".join(long_list[i: i + step])
            + "})"
        )
    return list_of_queries


def create_localized_queries(
    original_query: str,
    list_of_country_identifiers: list,
    search_field: str = 'TITLE-ABS-KEY',
    nr_identifiers_per_query: int = 20,
    universe: list = countries+demonyms,
) -> list:
    """
    This function takes a query and a list of country identifiers and returns a
    list of queries, each one of which is the original query with the addition
    of a number of country identifiers. The country identifiers are taken from
    the list provided as an argument.
    The function also returns a list of queries that are the complement of the
    first list with respect to the argument universe, i.e. the original query
    with the addition of all the country identifiers that are not in the list
    provided as an argument.
    """
    list_of_localized_queries = scopus_query_list_constructor(
        initial_query=original_query,
        long_list=list_of_country_identifiers,
        search_field=search_field,
        step=nr_identifiers_per_query,
    )
    list_of_country_identifiers_complement = [
        identifier for identifier in universe
        if identifier not in list_of_country_identifiers
    ]
    list_of_localized_queries_complement = scopus_query_list_constructor(
        initial_query=original_query,
        long_list=list_of_country_identifiers_complement,
        search_field=search_field,
        step=nr_identifiers_per_query,
    )
    return {
        'localized_queries': list_of_localized_queries,
        'localized_queries_complement': list_of_localized_queries_complement,
    }


# Localization bias tool
def localization_bias_tool(
        query: str,
        max_date: str,
        list_of_country_identifiers: list = weird_countries+weird_demonyms,
        ) -> pd.DataFrame:
    """
    This function takes a query and a list of country identifiers and returns
    a dataframe with the results of the query localized in the countries
    specified in the list of country identifiers, as well as in the remaining
    countries.
    """
    # Create localized queries
    localized_queries_dict = create_localized_queries(
        original_query=query,
        list_of_country_identifiers=list_of_country_identifiers,
        search_field='TITLE-ABS-KEY',
        nr_identifiers_per_query=20,
        universe=countries+demonyms,
    )
    # Retrieve localized records
    data_localized_weird = retrieve_results_from_list_of_queries(
        list_of_queries=localized_queries_dict['localized_queries'],
        max_date=max_date,
    )
    data_localized_no_weird = retrieve_results_from_list_of_queries(
        list_of_queries=localized_queries_dict['localized_queries_complement'],
        max_date=max_date,
    )
    # Concatenate data from weird and non-weird countries
    data_localized = pd.concat(
        [data_localized_weird, data_localized_no_weird]
    ).drop_duplicates(
        subset=['dc:identifier']
    ).reset_index(drop=True)
    # Label records based on whether they are from the list of countries or not
    data_localized['localized_weird'] = \
        data_localized['dc:identifier'].isin(
            data_localized_weird['dc:identifier'])
    data_localized['localized_no_weird'] = \
        data_localized['dc:identifier'].isin(
            data_localized_no_weird['dc:identifier'])
    # Add column 'localization_in_title' (boolean)
    data_localized = determine_localization_in_title(data_localized)
    return data_localized
