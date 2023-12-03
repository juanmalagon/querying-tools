import env_variables

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

st.write("Unbiased Request - SCOPUS")

if st.checkbox("Load example query"):
    st.session_state.original_query = mergoni_2021_scopus_query
    st.session_state.max_date = max_date

st.text_input("Insert your original query", key="original_query")
st.text_input("Insert a max date for extra filtering", key="max_date")

st.write("This is your original query:")
st.session_state.original_query
st.write("This is your max date for extra filtering:")
st.session_state.max_date


@st.cache_data
def load_data(query, max_date):
    data = retrieve_results_from_list_of_queries(
        list_of_queries=[query], max_date=max_date
    )
    return data


if st.checkbox("Retrieve data from your original query and load it into cache"
               ):
    data_load_state = st.text("Loading data for your query...")
    data_original = load_data(
        st.session_state.original_query, st.session_state.max_date
    )
    data_load_state.text(
        f"Data loaded! Retrieved {len(data_original)} results.")

    if st.checkbox("Show original data head"):
        st.subheader("Original query data head")
        st.write(data_original.head(5))

st.session_state.lang_bias_query = language_bias_helper(
    st.session_state.original_query)
st.session_state.pub_bias_query = publication_bias_helper(
    st.session_state.original_query
)

st.write("This is your query without language bias:")
st.session_state.lang_bias_query

if st.checkbox("Retrieve data from your query without language bias"):
    data_load_state = st.text("Loading data for your query...")
    data_lang = load_data(
        st.session_state.lang_bias_query, st.session_state.max_date)
    data_load_state.text(f"Data loaded! Retrieved {len(data_lang)} results.")

    if st.checkbox("Show language helper data head"):
        st.subheader("Language helper query data head")
        st.write(data_lang.head(5))

st.write("This is your query without publication bias:")
st.session_state.pub_bias_query

if st.checkbox("Retrieve data from your query without publication bias"):
    data_load_state = st.text("Loading data for your query...")
    data_pub = load_data(
        st.session_state.pub_bias_query, st.session_state.max_date)
    data_load_state.text(f"Data loaded! Retrieved {len(data_pub)} results.")

    if st.checkbox("Show publication helper data head"):
        st.subheader("Publication helper query data head")
        st.write(data_pub.head(5))
