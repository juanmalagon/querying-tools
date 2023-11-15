import logging
import re
import pandas as pd

from utils import country_lists as cl
from utils import examples as ex

# from utils.functions import scopus_query_list_constructor

# Scopus
# For help on using the Scopus Search API, see:
# https://dev.elsevier.com/documentation/ScopusSearchAPI
# Scopus search tips:
# https://dev.elsevier.com/sc_search_tips.html

module_logger = logging.getLogger("main.utils.query_helpers")


def language_bias_helper(query: str) -> str:
    """
    Returns a query without the language restriction.
    """
    return re.sub(r"(AND\s)*LANGUAGE\(\w+\)", "", query)


def publication_bias_helper(query: str) -> str:
    """
    Returns a query without the language restriction.
    """
    return re.sub(r"(AND\s)*SRCTYPE\(\w+\)", "", query)


def find_localization_in_text(
    text: str, countries: list[str] = cl.countries, demonyms: list[str] = cl.demonyms
) -> bool:
    """
    Returns True if any country name or demonym is found in the text.
    """
    text_words = text.lower().split()
    if any(location.lower() in text_words for location in countries + demonyms):
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
    df_copy["localization_in_title"] = df["dc:title"].apply(find_localization_in_text)
    return df_copy


# # Original query by the authors
# scopus_original_query = ex.mergoni_2021_scopus_query

# # Language-bias-helper: initial query after removing the language restriction
# scopus_lang_bias_helper_query = language_bias_helper(scopus_original_query)

# # Localization-bias-helper: queries including country names and demonyms
# # Queries for Western, Educated, Industrialized, Rich and Democratic (WEIRD)
# # countries
# scopus_local_bias_helper_queries__weird_countries = scopus_query_list_constructor(
#     scopus_original_query, cl.weird_countries, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_helper_queries__weird_demonyms = scopus_query_list_constructor(
#     scopus_original_query, cl.weird_demonyms, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_helper_queries_weird = (
#     scopus_local_bias_helper_queries__weird_countries
#     + scopus_local_bias_helper_queries__weird_demonyms
# )
# # Queries for non-WEIRD countries
# scopus_local_bias_helper_queries__non_weird_countries = scopus_query_list_constructor(
#     scopus_original_query, cl.non_weird_countries, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_helper_queries__non_weird_demonyms = scopus_query_list_constructor(
#     scopus_original_query, cl.non_weird_demonyms, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_helper_queries_non_weird = (
#     scopus_local_bias_helper_queries__non_weird_countries
#     + scopus_local_bias_helper_queries__non_weird_demonyms
# )
# # Queries for Latin American and Caribbean (LAC) countries
# scopus_local_bias_helper_queries__lac_countries = scopus_query_list_constructor(
#     scopus_original_query, cl.lac_countries, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_helper_queries__lac_demonyms = scopus_query_list_constructor(
#     scopus_original_query, cl.lac_demonyms, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_helper_queries_lac = (
#     scopus_local_bias_helper_queries__lac_countries
#     + scopus_local_bias_helper_queries__lac_demonyms
# )

# Publication-bias-helper: queries including the grey literature
scopus_pub_bias_helper_query = (
    "ALL({data envelopment analysis})"
    + " AND ALL({policy evaluation})"
    + " AND PUBYEAR > 1956"
    + " AND PUBYEAR < 2022"
    + " AND LANGUAGE(english)"
)
