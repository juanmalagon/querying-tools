import logging

from utils import country_lists as cl
from utils.functions import scopus_query_list_constructor

# Scopus
# For help on using the Scopus Search API, see:
# https://dev.elsevier.com/documentation/ScopusSearchAPI

module_logger = logging.getLogger('main.utils.queries')

# Original query by the authors
mergoni_scopus_original_query = 'ALL({data envelopment analysis})' +\
  ' AND ALL({policy evaluation})' +\
  ' AND PUBYEAR > 1956' +\
  ' AND PUBYEAR < 2022' +\
  ' AND LANGUAGE(english)' +\
  ' AND SRCTYPE(j)'

# Language-bias-helper: initial query after removing the language restriction
mergoni_scopus_lang_bias_helper_query = 'ALL({data envelopment analysis})' +\
  ' AND ALL({policy evaluation})' +\
  ' AND PUBYEAR > 1956' +\
  ' AND PUBYEAR < 2022' +\
  ' AND SRCTYPE(j)'

# Localization-bias-helper: queries including country names and demonyms
# Queries for Western, Educated, Industrialized, Rich and Democratic (WEIRD)
# countries
mergoni_scopus_local_bias_helper_queries__weird_countries = (
    scopus_query_list_constructor(
        mergoni_scopus_original_query, cl.weird_countries, step=20,
        search_field='TITLE-ABS-KEY'))
mergoni_scopus_local_bias_helper_queries__weird_demonyms = (
    scopus_query_list_constructor(
        mergoni_scopus_original_query, cl.weird_demonyms, step=20,
        search_field='TITLE-ABS-KEY'))
mergoni_scopus_local_bias_helper_queries_weird =\
  mergoni_scopus_local_bias_helper_queries__weird_countries +\
  mergoni_scopus_local_bias_helper_queries__weird_demonyms
# Queries for non-WEIRD countries
mergoni_scopus_local_bias_helper_queries__non_weird_countries =\
    scopus_query_list_constructor(mergoni_scopus_original_query,
                                  cl.non_weird_countries,
                                  step=20, search_field='TITLE-ABS-KEY')
mergoni_scopus_local_bias_helper_queries__non_weird_demonyms =\
    scopus_query_list_constructor(mergoni_scopus_original_query,
                                  cl.non_weird_demonyms,
                                  step=20, search_field='TITLE-ABS-KEY')
mergoni_scopus_local_bias_helper_queries_non_weird =\
    mergoni_scopus_local_bias_helper_queries__non_weird_countries +\
    mergoni_scopus_local_bias_helper_queries__non_weird_demonyms
# Queries for Latin American and Caribbean (LAC) countries
mergoni_scopus_local_bias_helper_queries__lac_countries = (
    scopus_query_list_constructor(
        mergoni_scopus_original_query, cl.lac_countries, step=20,
        search_field='TITLE-ABS-KEY'))
mergoni_scopus_local_bias_helper_queries__lac_demonyms = (
    scopus_query_list_constructor(
        mergoni_scopus_original_query, cl.lac_demonyms, step=20,
        search_field='TITLE-ABS-KEY'))
mergoni_scopus_local_bias_helper_queries_lac =\
  mergoni_scopus_local_bias_helper_queries__lac_countries +\
  mergoni_scopus_local_bias_helper_queries__lac_demonyms

# Publication-bias-helper: queries including the grey literature
mergoni_scopus_pub_bias_helper_query = 'ALL({data envelopment analysis})' +\
  ' AND ALL({policy evaluation})' +\
  ' AND PUBYEAR > 1956' +\
  ' AND PUBYEAR < 2022' +\
  ' AND LANGUAGE(english)'
