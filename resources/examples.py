# Example queries

# Recreation of the queries documented by various literature
# reviews on efficiency of education

mergoni_2021_scopus_query = (
    "ALL({data envelopment analysis})"
    + " AND ALL({policy evaluation})"
    + " AND PUBYEAR > 1956"
    + " AND PUBYEAR < 2022"
    + " AND LANGUAGE(english)"
    + " AND SRCTYPE(j)"
)

mergoni_2021_max_date = "2021-02-01"


haddad_2021_scopus_query = (
    "TITLE-ABS-KEY({school performance})"  # review this search
    + " AND TITLE-ABS-KEY({education efficiency})"
    + " AND TITLE-ABS-KEY({input output variables})"
    + " AND PUBYEAR > 2010"
    + " AND PUBYEAR < 2020"
    + " AND LANGUAGE(english)"
    + " AND SRCTYPE(j)"
)

haddad_2021_max_date = "2021-02-01"


villano_2021_scopus_query = (
    "ALL({data envelopment analysis})"
    + " AND ALL({policy evaluation})"
    + " AND PUBYEAR > 1956"
    + " AND PUBYEAR < 2022"
    + " AND LANGUAGE(english)"
    + " AND SRCTYPE(j)"
)

villano_2021_max_date = "2021-02-01"
