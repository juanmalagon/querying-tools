from resources.examples import mergoni_2021_scopus_query, max_date
from resources.helper_tools import (
    language_bias_helper,
    publication_bias_helper,
)
from resources.scopus_functions import (
    retrieve_results_from_list_of_queries,
)
import logging
import streamlit as st


# Set up logging
# Create logger with 'main'
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
# Create file handler which logs even debug messages
fh = logging.FileHandler('main.log')
fh.setLevel(logging.DEBUG)
# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# Create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - [%(module)s|%(funcName)s] - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# Set up Streamlit

st.markdown(
    """
    # Unbiased Requester

    This app allows you to retrieve data from
    <a href="https://www.scopus.com/">
    Scopus
    </a>
    and compare the results from
    your original query with the results from queries without language and
    publication bias.

    ## How to use it

    1. Insert your original query in the first text box (for help on how to
    create your query string see <a
    href="https://dev.elsevier.com/sc_search_tips.html">Scopus search tips </a>
    and <a href="https://dev.elsevier.com/documentation/ScopusSearchAPI">Scopus
    Search API</a>).
    2. Insert a maximum date for extra filtering (optional).
    3. If you want to load an example query and maximum date for extra
    filtering, check the box below.
    4. Click on the checkbox "Retrieve data from your original query".
    5. Click on the checkbox "Apply language-bias-helper and retrieve data
    from your query".
    6. Click on the checkbox "Apply publication-bias-helper and retrieve data
    from your query".
    """,
    unsafe_allow_html=True,
)
# st.write("Unbiased Requester - SCOPUS")
# st.write("This app allows you to retrieve data from Scopus and compare the \
#     results from your original query with the results from queries without \
#         language and publication bias.")

# "st.session_state object:", st.session_state

st.text_input("Insert your original query", key="original_query")
st.text_input("Insert a maximum date for extra filtering (optional)",
              key="max_date")

# st.write(st.session_state)

if st.checkbox("Load an example query and maximum date for extra filtering \
               (Mergoni and De Witte, 2022)"):
    del st.session_state.original_query
    del st.session_state.max_date
    st.session_state.original_query = mergoni_2021_scopus_query
    st.session_state.max_date = max_date

"This is your original query: ", st.session_state.original_query
"This is your maximum date for extra filtering:", st.session_state.max_date


@st.cache_data
def load_data(query, max_date):
    data = retrieve_results_from_list_of_queries(
        list_of_queries=[query], max_date=max_date
    )
    return data


if st.checkbox("Retrieve data from your original query"
               ):
    data_load_state = st.text(
        "Loading data for your query... This may take a few minutes")
    data_original = load_data(
        st.session_state.original_query, st.session_state.max_date
    )
    data_load_state.text(
        f"Data loaded! Retrieved {len(data_original)} results.")

    if st.checkbox("Show original data head"):
        st.write("Original query data head")
        st.write(data_original.head(5))

st.session_state.lang_bias_query = language_bias_helper(
    st.session_state.original_query)
st.session_state.pub_bias_query = publication_bias_helper(
    st.session_state.original_query
)

# st.write("This is your query without language bias:")
# st.session_state.lang_bias_query

if st.checkbox("Apply language-bias-helper and retrieve data from your query"):
    data_load_state = st.text(
        "Loading data for your query... This may take a few minutes")
    data_lang = load_data(
        st.session_state.lang_bias_query, st.session_state.max_date)
    data_load_state.text(f"Data loaded! Retrieved {len(data_lang)} results.")

    if st.checkbox("Show language-bias-helper data head"):
        st.write("Language-bias-helper data head")
        st.write(data_lang.head(5))

# st.write("This is your query without publication bias:")
# st.session_state.pub_bias_query

if st.checkbox("Apply publication-bias-helper and retrieve data from your\
                query"):
    data_load_state = st.text(
        "Loading data for your query... This may take a few minutes")
    data_pub = load_data(
        st.session_state.pub_bias_query, st.session_state.max_date)
    data_load_state.text(f"Data loaded! Retrieved {len(data_pub)} results.")

    if st.checkbox("Show publication-bias-helper data head"):
        st.write("Publication-bias-helper data head")
        st.write(data_pub.head(5))
