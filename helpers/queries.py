from helpers import country_lists as cl


def scopus_query_list_constructor(initial_query, long_list, step=20):
    list_of_queries = []
    for i in range(0, len(long_list), step):
        list_of_queries.append(
            initial_query + ' AND ALL({' + '} OR {'.join(long_list[i:i+20]) +
            '})')
    return list_of_queries


# scopus
mergoni_scopus_query = 'ALL({data envelopment analysis})' +\
  ' AND ALL({policy evaluation})' +\
  ' AND PUBYEAR > 1956' +\
  ' AND PUBYEAR < 2022' +\
  ' AND LANGUAGE(english)' +\
  ' AND SRCTYPE(j)'
mergoni_scopus_step_1_query = 'ALL({data envelopment analysis})' +\
  ' AND ALL({policy evaluation})' +\
  ' AND PUBYEAR > 1956' +\
  ' AND PUBYEAR < 2022' +\
  ' AND SRCTYPE(j)'
mergoni_scopus_step_2_queries__countries = scopus_query_list_constructor(
    mergoni_scopus_query, cl.countries)
mergoni_scopus_step_2_queries__demonyms = scopus_query_list_constructor(
    mergoni_scopus_query, cl.demonyms)
