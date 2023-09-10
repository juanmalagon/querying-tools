from helpers import country_lists as cl

# Scopus
# For help on using the Scopus Search API, see:
# https://dev.elsevier.com/documentation/ScopusSearchAPI


def scopus_query_list_constructor(initial_query: str,
                                  long_list: list[str],
                                  search_field: str = 'ALL',
                                  step: int = 20):
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
            initial_query + ' AND ' + search_field + '({' +
            '} OR {'.join(long_list[i:i+20]) +
            '})'
            )
    return list_of_queries


# Step 0: initial query by the authors
mergoni_scopus_original_query = 'ALL({data envelopment analysis})' +\
  ' AND ALL({policy evaluation})' +\
  ' AND PUBYEAR > 1956' +\
  ' AND PUBYEAR < 2022' +\
  ' AND LANGUAGE(english)' +\
  ' AND SRCTYPE(j)'

# Step 1: initial query after removing the language restriction
mergoni_scopus_lang_bias_helper_query = 'ALL({data envelopment analysis})' +\
  ' AND ALL({policy evaluation})' +\
  ' AND PUBYEAR > 1956' +\
  ' AND PUBYEAR < 2022' +\
  ' AND SRCTYPE(j)'

# Step 2: queries including country names and demonyms

# Queries for Western, Educated, Industrialized, Rich and Democratic (WEIRD)
# countries

mergoni_scopus_local_bias_helper_queries__weird_countries = (
    scopus_query_list_constructor(
        mergoni_scopus_original_query, cl.weird_countries, step=20,
        search_field='TITLE-ABS'))
mergoni_scopus_local_bias_helper_queries__weird_demonyms = (
    scopus_query_list_constructor(
        mergoni_scopus_original_query, cl.weird_demonyms, step=20,
        search_field='TITLE-ABS'))
mergoni_scopus_local_bias_helper_queries_weird =\
  mergoni_scopus_local_bias_helper_queries__weird_countries +\
  mergoni_scopus_local_bias_helper_queries__weird_demonyms

# Queries for non-WEIRD countries

mergoni_scopus_local_bias_helper_queries__non_weird_countries =\
    scopus_query_list_constructor(mergoni_scopus_original_query,
                                  cl.non_weird_countries,
                                  step=20, search_field='TITLE-ABS')
mergoni_scopus_local_bias_helper_queries__non_weird_demonyms =\
    scopus_query_list_constructor(mergoni_scopus_original_query,
                                  cl.non_weird_demonyms,
                                  step=20, search_field='TITLE-ABS')
mergoni_scopus_local_bias_helper_queries_non_weird =\
    mergoni_scopus_local_bias_helper_queries__non_weird_countries +\
    mergoni_scopus_local_bias_helper_queries__non_weird_demonyms

# Queries for Latin American and Caribbean (LAC) countries

mergoni_scopus_local_bias_helper_queries__lac_countries = (
    scopus_query_list_constructor(
        mergoni_scopus_original_query, cl.lac_countries, step=20,
        search_field='TITLE-ABS'))
mergoni_scopus_local_bias_helper_queries__lac_demonyms = (
    scopus_query_list_constructor(
        mergoni_scopus_original_query, cl.lac_demonyms, step=20,
        search_field='TITLE-ABS'))
mergoni_scopus_local_bias_helper_queries_lac =\
  mergoni_scopus_local_bias_helper_queries__lac_countries +\
  mergoni_scopus_local_bias_helper_queries__lac_demonyms
