# # Original query by the authors
# scopus_original_query = ex.mergoni_2021_scopus_query

# # Language-bias-tool: initial query after removing the language restriction
# scopus_lang_bias_tool_query = language_bias_tool(scopus_original_query)

# # Localization-bias-tool: queries including country names and demonyms
# # Queries for Western, Educated, Industrialized, Rich and Democratic (WEIRD)
# # countries
# scopus_local_bias_tool_queries__weird_countries = \
#     scopus_query_list_constructor(
#         scopus_original_query,
#         cl.weird_countries, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_tool_queries__weird_demonyms = scopus_query_list_constructor(
#     scopus_original_query, cl.weird_demonyms, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_tool_queries_weird = (
#     scopus_local_bias_tool_queries__weird_countries
#     + scopus_local_bias_tool_queries__weird_demonyms
# )
# # Queries for non-WEIRD countries
# scopus_local_bias_tool_queries__non_weird_countries = scopus_query_list_constructor(
#     scopus_original_query, cl.non_weird_countries, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_tool_queries__non_weird_demonyms = scopus_query_list_constructor(
#     scopus_original_query, cl.non_weird_demonyms, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_tool_queries_non_weird = (
#     scopus_local_bias_tool_queries__non_weird_countries
#     + scopus_local_bias_tool_queries__non_weird_demonyms
# )
# # Queries for Latin American and Caribbean (LAC) countries
# scopus_local_bias_tool_queries__lac_countries = scopus_query_list_constructor(
#     scopus_original_query, cl.lac_countries, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_tool_queries__lac_demonyms = scopus_query_list_constructor(
#     scopus_original_query, cl.lac_demonyms, step=20, search_field="TITLE-ABS-KEY"
# )
# scopus_local_bias_tool_queries_lac = (
#     scopus_local_bias_tool_queries__lac_countries
#     + scopus_local_bias_tool_queries__lac_demonyms
# )