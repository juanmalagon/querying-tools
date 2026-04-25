from resources.examples import mergoni_2021_scopus_query, mergoni_2021_max_date
from resources.querying_tools import (
    language_bias_tool,
    publication_bias_tool,
    localization_bias_tool,
)
from resources.scopus_functions import (
    retrieve_results_from_list_of_queries,
    columns_to_hide,
)
from app_config import settings
import logging
import streamlit as st


# Set up logging
# Create logger with 'main'
logger = logging.getLogger("querying_tools")
logger.setLevel(getattr(logging, settings.log_level, logging.INFO))
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - [%(module)s|%(funcName)s] - %(levelname)s - %(message)s"
        )
    )
    logger.addHandler(handler)
logger.propagate = False

# Set up Streamlit

# Instructions

st.markdown(
    """
    # Unbiased Requester

    This app allows you to retrieve data from
    <a href="https://www.scopus.com/">Scopus</a> and then apply a set of
    querying tools to assess language, publication, availability and
    localization bias from your original query.

    The app is the accompanying material of the paper:

    Malagon J, Haelermans C. _Reading between the lines: biases and
    reproducibility challenges in efficiency of education reviews. 2023_


    ### How to use it

    1. Insert your original query string in the first text box (for help on how
    to create your query string see <a
    href="https://dev.elsevier.com/sc_search_tips.html"> Scopus search tips
    </a>).\n
    \t (Optional: Insert a maximum date in the second text box for extra
    filtering . This date usually corresponds to the publication date of the
    paper you are reviewing or writing).\n
    \t If you rather prefer to load an example query and maximum date for extra
    filtering, check the box below.
    2. Click on the checkbox "Retrieve data from your original query" to
    retrieve data from your original query.
    3. Click on the checkbox "Apply language-bias-tool" to retrieve data from
    your original query without language bias.
    4. Click on the checkbox "Apply publication-bias-tool" to retrieve data
    from your original query without publication bias.
    """,
    unsafe_allow_html=True,
)

if not settings.has_scopus_credentials():
    st.warning(
        "Scopus credentials are not configured yet. Set the `SCOPUS_API_KEY` "
        "environment variable or add `scopus/config.json` before retrieving data."
    )

st.markdown(
    """
    ### Retrieve data
    """,
    unsafe_allow_html=True,
)
st.text_input("Insert your original query", key="original_query")
st.text_input("(Optional: Insert a maximum date for extra filtering)", key="max_date")

if st.checkbox(
    "Load an example query and maximum date for extra filtering \
               (Mergoni and De Witte, 2022)"
):
    st.session_state.pop("original_query", None)
    st.session_state.pop("max_date", None)
    st.session_state.original_query = mergoni_2021_scopus_query
    st.session_state.max_date = mergoni_2021_max_date

"This is your original query:"
st.session_state.original_query
"This is your maximum date for extra filtering:"
st.session_state.max_date


@st.cache_data
def load_data(query, max_date):
    data = retrieve_results_from_list_of_queries(
        list_of_queries=[query], max_date=max_date
    )
    return data


def get_current_inputs():
    query = st.session_state.get("original_query", "").strip()
    max_date = st.session_state.get("max_date", "").strip() or None
    if not query:
        st.error("Enter a Scopus query or load the example query before retrieving data.")
        return None, None
    return query, max_date


def get_original_data():
    query, max_date = get_current_inputs()
    if not query:
        return None
    return load_data(query, max_date)


def show_data_error(error: Exception) -> None:
    logger.exception("Data retrieval failed")
    st.error(f"Unable to retrieve data: {error}")


def safe_percentage(part: int, total: int) -> float:
    return round(100 * part / total, 1) if total else 0.0


@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")


# Retrieve data from original query

if st.checkbox("Retrieve data from your original query"):
    data_load_state = st.text("Loading data for your query... This may take a few minutes")
    try:
        data_original = get_original_data()
    except Exception as exc:
        data_load_state.empty()
        show_data_error(exc)
    else:
        if data_original is not None:
            data_load_state.text(f"Data loaded! Retrieved {len(data_original)} results.")
            data_original_to_display = data_original.drop(columns=columns_to_hide, errors="ignore")
            if st.checkbox("\t Show original data"):
                st.write("Original query data")
                st.write(data_original_to_display)
                st.download_button(
                    "Download CSV",
                    convert_df(data_original_to_display),
                    "original_query_data",
                    "text/csv",
                    key="download_original_query_data",
                )

st.markdown(
    """
    ### Apply querying tools
    """,
    unsafe_allow_html=True,
)

st.session_state.lang_bias_query = language_bias_tool(
    st.session_state.get("original_query", "")
)
st.session_state.pub_bias_query = publication_bias_tool(
    st.session_state.get("original_query", "")
)

# Language bias tool

if st.checkbox("Apply language-bias-tool"):
    data_load_state = st.text("Loading data for your query... This may take a few minutes")
    try:
        data_original = get_original_data()
        if data_original is None:
            data_load_state.empty()
        else:
            data_lang = load_data(st.session_state.lang_bias_query, st.session_state.max_date)
            data_load_state.text(
                "Data loaded!\n"
                + f"Retrieved {len(data_lang)} results from language-bias-tool.\n"
                + "This means the tool retrieved "
                + f"{len(data_lang) - len(data_original)} additional records."
            )
            if st.checkbox("\t Show language-bias-tool additional records"):
                data_lang_diff = data_lang[
                    ~data_lang["dc:identifier"].isin(data_original["dc:identifier"])
                ].reset_index(drop=True)
                data_lang_diff_to_display = data_lang_diff.drop(columns=columns_to_hide, errors="ignore")
                st.write("Language-bias-tool data")
                st.write(data_lang_diff_to_display)
                st.download_button(
                    "Download CSV",
                    convert_df(data_lang_diff_to_display),
                    "lang_bias_tool_data",
                    "text/csv",
                    key="download_lang_bias_tool_data",
                )
    except Exception as exc:
        data_load_state.empty()
        show_data_error(exc)

# Publication bias tool

if st.checkbox("Apply publication-bias-tool"):
    data_load_state = st.text("Loading data for your query... This may take a few minutes")
    try:
        data_original = get_original_data()
        if data_original is None:
            data_load_state.empty()
        else:
            data_pub = load_data(st.session_state.pub_bias_query, st.session_state.max_date)
            data_load_state.text(
                "Data loaded!\n"
                + f"Retrieved {len(data_pub)} results from publication-bias-tool.\n"
                + "This means the tool retrieved "
                + f"{len(data_pub) - len(data_original)} additional records."
            )

            if st.checkbox("\t Show publication-bias-tool data additional records"):
                data_pub_diff = data_pub[
                    ~data_pub["dc:identifier"].isin(data_original["dc:identifier"])
                ].reset_index(drop=True)
                data_pub_diff_to_display = data_pub_diff.drop(columns=columns_to_hide, errors="ignore")
                st.write("Publication-bias-tool data")
                st.write(data_pub_diff_to_display)
                st.download_button(
                    "Download CSV",
                    convert_df(data_pub_diff_to_display),
                    "pub_bias_tool_data",
                    "text/csv",
                    key="download_pub_bias_tool_data",
                )
    except Exception as exc:
        data_load_state.empty()
        show_data_error(exc)

# Localization bias tool

if st.checkbox("Apply localization-bias-tool"):
    data_load_state = st.text("Loading data for your query... This may take a few minutes")
    try:
        query, max_date = get_current_inputs()
        if not query:
            data_load_state.empty()
        else:
            data_localized = localization_bias_tool(query, max_date)
            data_localized__weird = data_localized[data_localized["localized_weird"]]
            data_localized__no_weird = data_localized[data_localized["localized_no_weird"]]
            nr_titles__weird = data_localized__weird["localization_in_title"].sum()
            nr_titles__no_weird = data_localized__no_weird["localization_in_title"].sum()

            data_load_state.text(
                "Data loaded!\n"
                + f"Retrieved {len(data_localized)} localized results with the "
                + "localization-bias-tool.\n"
                + f"{len(data_localized__weird)} results come from WEIRD countries, \n"
                + f" but only {nr_titles__weird} of these have localization in title "
                + f"({safe_percentage(nr_titles__weird, len(data_localized__weird))}%).\n"
                + f"{len(data_localized__no_weird)} results come from non-WEIRD "
                + "countries, \n but only "
                + f"{nr_titles__no_weird} of these have localization in title "
                + f"({safe_percentage(nr_titles__no_weird, len(data_localized__no_weird))}%)."
            )
            data_localized_to_display = data_localized.drop(columns=columns_to_hide, errors="ignore")

            if st.checkbox("\t Show localization-bias-tool data records"):
                st.write("Localization-bias-tool data")
                st.write(data_localized_to_display)
                st.download_button(
                    "Download CSV",
                    convert_df(data_localized_to_display),
                    "localization_bias_tool_data",
                    "text/csv",
                    key="download_localization_bias_tool_data",
                )
    except Exception as exc:
        data_load_state.empty()
        show_data_error(exc)

# Availability bias tool

if st.checkbox("Apply availability-bias-tool"):
    data_load_state = st.text("Loading data for your query... This may take a few minutes")
    try:
        data_available = get_original_data()
        if data_available is None:
            data_load_state.empty()
        else:
            data_available = data_available.copy()
            nr_open_access_records = int(data_available["openaccess"].fillna(False).astype(bool).sum())
            availability_benchmark = safe_percentage(nr_open_access_records, len(data_available))
            data_load_state.text(
                "Data loaded!\n"
                + f"Retrieved {len(data_available)} results with the "
                + " availability-bias-tool.\n"
                + "Out of these results "
                + f"{nr_open_access_records} are open-access records.\n"
                + f"This corresponds to {availability_benchmark}% of the total records."
            )

            if st.checkbox("\t Show availability-bias-tool data records"):
                data_available_diff = data_available[data_available["openaccess"]].reset_index(
                    drop=True
                )
                st.write("Availability-bias-tool data")
                st.write(data_available_diff)
                st.download_button(
                    "Download CSV",
                    convert_df(data_available_diff),
                    "availability_bias_tool_data",
                    "text/csv",
                    key="download_availability_bias_tool_data",
                )
    except Exception as exc:
        data_load_state.empty()
        show_data_error(exc)
