import logging

from utils import country_lists as cl
from utils.scopus_functions import scopus_query_list_constructor

# Scopus
# For help on using the Scopus Search API, see:
# https://dev.elsevier.com/documentation/ScopusSearchAPI
# Scopus search tips:
# https://dev.elsevier.com/sc_search_tips.html

module_logger = logging.getLogger("main.utils.queries")

# Original query by the authors
scopus_original_query = (
    "ALL({data envelopment analysis})"
    + " AND ALL({policy evaluation})"
    + " AND PUBYEAR > 1956"
    + " AND PUBYEAR < 2022"
    + " AND LANGUAGE(english)"
    + " AND SRCTYPE(j)"
)

# Language-bias-tool: initial query after removing the language restriction
scopus_lang_bias_tool_query = (
    "ALL({data envelopment analysis})"
    + " AND ALL({policy evaluation})"
    + " AND PUBYEAR > 1956"
    + " AND PUBYEAR < 2022"
    + " AND SRCTYPE(j)"
)

# Localization-bias-tool: queries including country names and demonyms
# Queries for Western, Educated, Industrialized, Rich and Democratic (WEIRD)
# countries
scopus_local_bias_tool_queries__weird_countries = scopus_query_list_constructor(
    scopus_original_query, cl.weird_countries, step=20, search_field="TITLE-ABS-KEY"
)
scopus_local_bias_tool_queries__weird_demonyms = scopus_query_list_constructor(
    scopus_original_query, cl.weird_demonyms, step=20, search_field="TITLE-ABS-KEY"
)
scopus_local_bias_tool_queries_weird = (
    scopus_local_bias_tool_queries__weird_countries
    + scopus_local_bias_tool_queries__weird_demonyms
)
# Queries for non-WEIRD countries
scopus_local_bias_tool_queries__non_weird_countries = scopus_query_list_constructor(
    scopus_original_query, cl.non_weird_countries, step=20, search_field="TITLE-ABS-KEY"
)
scopus_local_bias_tool_queries__non_weird_demonyms = scopus_query_list_constructor(
    scopus_original_query, cl.non_weird_demonyms, step=20, search_field="TITLE-ABS-KEY"
)
scopus_local_bias_tool_queries_non_weird = (
    scopus_local_bias_tool_queries__non_weird_countries
    + scopus_local_bias_tool_queries__non_weird_demonyms
)
# Queries for Latin American and Caribbean (LAC) countries
scopus_local_bias_tool_queries__lac_countries = scopus_query_list_constructor(
    scopus_original_query, cl.lac_countries, step=20, search_field="TITLE-ABS-KEY"
)
scopus_local_bias_tool_queries__lac_demonyms = scopus_query_list_constructor(
    scopus_original_query, cl.lac_demonyms, step=20, search_field="TITLE-ABS-KEY"
)
scopus_local_bias_tool_queries_lac = (
    scopus_local_bias_tool_queries__lac_countries
    + scopus_local_bias_tool_queries__lac_demonyms
)

# Publication-bias-tool: queries including the grey literature
scopus_pub_bias_tool_query = (
    "ALL({data envelopment analysis})"
    + " AND ALL({policy evaluation})"
    + " AND PUBYEAR > 1956"
    + " AND PUBYEAR < 2022"
    + " AND LANGUAGE(english)"
)
