from helpers import country_lists as cl


def scopus_query_list_constructor(initial_query: str,
                                  long_list: list[str],
                                  search_field: str = 'ALL',
                                  step: int = 20):
    list_of_queries = []
    for i in range(0, len(long_list), step):
        list_of_queries.append(
            initial_query + ' AND ' + search_field + '({' +
            '} OR {'.join(long_list[i:i+20]) +
            '})'
            )
    return list_of_queries


# Scopus
# For help on using the Scopus Search API, see:
# https://dev.elsevier.com/documentation/ScopusSearchAPI.wadl

# Step 0: initial query
mergoni_scopus_query = 'ALL({data envelopment analysis})' +\
  ' AND ALL({policy evaluation})' +\
  ' AND PUBYEAR > 1956' +\
  ' AND PUBYEAR < 2022' +\
  ' AND LANGUAGE(english)' +\
  ' AND SRCTYPE(j)'

# Step 1: remove language restriction
mergoni_scopus_step_1_query = 'ALL({data envelopment analysis})' +\
  ' AND ALL({policy evaluation})' +\
  ' AND PUBYEAR > 1956' +\
  ' AND PUBYEAR < 2022' +\
  ' AND SRCTYPE(j)'

# Step 2: assess country and demonyms prevalence
# Queries for Western, Educated, Industrialized, Rich and Democratic (WEIRD)
# countries
mergoni_scopus_step_2_queries__weird_countries = scopus_query_list_constructor(
    mergoni_scopus_query, cl.weird_countries, step=20,
    search_field='TITLE-ABS')
mergoni_scopus_step_2_queries__weird_demonyms = scopus_query_list_constructor(
    mergoni_scopus_query, cl.weird_demonyms, step=20,
    search_field='TITLE-ABS')
mergoni_scopus_step_2_queries_weird =\
  mergoni_scopus_step_2_queries__weird_countries +\
  mergoni_scopus_step_2_queries__weird_demonyms

# Queries for non-WEIRD countries
mergoni_scopus_step_2_queries__non_weird_countries =\
    scopus_query_list_constructor(mergoni_scopus_query, cl.non_weird_countries,
                                  step=20, search_field='TITLE-ABS')
mergoni_scopus_step_2_queries__non_weird_demonyms =\
    scopus_query_list_constructor(mergoni_scopus_query, cl.non_weird_demonyms,
                                  step=20, search_field='TITLE-ABS')
mergoni_scopus_step_2_queries_non_weird =\
    mergoni_scopus_step_2_queries__non_weird_countries +\
    mergoni_scopus_step_2_queries__non_weird_demonyms

# Queries for Latin American and Caribbean (LAC) countries
mergoni_scopus_step_2_queries__lac_countries = scopus_query_list_constructor(
    mergoni_scopus_query, cl.lac_countries, step=20, search_field='TITLE-ABS')
mergoni_scopus_step_2_queries__lac_demonyms = scopus_query_list_constructor(
    mergoni_scopus_query, cl.lac_demonyms, step=20, search_field='TITLE-ABS')
mergoni_scopus_step_2_queries_lac =\
  mergoni_scopus_step_2_queries__lac_countries +\
  mergoni_scopus_step_2_queries__lac_demonyms

mergoni_scopus_step_2_queries__countries = scopus_query_list_constructor(
    mergoni_scopus_query, cl.countries, step=20, search_field='ALL')
mergoni_scopus_step_2_queries__demonyms = scopus_query_list_constructor(
    mergoni_scopus_query, cl.demonyms, step=20, search_field='ALL')
