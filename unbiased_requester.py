import streamlit as st

###############################################
import os

# Define environment variables

# Change 'project_dir' to your project directory
os.environ["project_dir"] = "/Users/juanmalagon/repos/unbiased-request"

# Change 'scopus_config_file' to your Scopus config file. See:
# https://dev.elsevier.com/documentation/AuthenticationAPI
os.environ["scopus_config_file"] = os.path.join(
    os.getenv("project_dir"), "scopus/config.json"
)

# Change 'scopus_data_dir' to your Scopus data directory:
# this is the place your Scopus retrieved data will be saved
os.environ["scopus_data_dir"] = os.path.join(os.getenv("project_dir"), "data/")
os.environ["save_to_csv"] = "1"

# Change working directory
os.chdir(os.getenv("project_dir"))

###############################################

# Lists for all countries
countries = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Comoros",
    "Congo",
    "Costa Rica",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czech Republic",
    "Czechia",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini",
    "Ethiopia",
    "Fiji",
    "Finland",
    "France",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "North Korea",
    "South Korea",
    "Korea",
    "Kosovo",
    "Kuwait",
    "Kyrgyzstan",
    "Laos",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Macedonia",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Russia",
    "Rwanda",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Syria",
    "Taiwan",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "UK",
    "United States",
    "USA",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Vatican City",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]

demonyms = [
    "Afghan",
    "Albanian",
    "Algerian",
    "Andorran",
    "Angolan",
    "Antiguan and Barbudan",
    "Argentinian",
    "Argentine",
    "Armenian",
    "Australian",
    "Austrian",
    "Azerbaijani",
    "Bahamian",
    "Bahraini",
    "Bangladeshi",
    "Barbadian",
    "Belarusian",
    "Belgian",
    "Belizean",
    "Beninese",
    "Bhutanese",
    "Bolivian",
    "Bosnian",
    "Botswanan",
    "Brazilian",
    "Bruneian",
    "Bulgarian",
    "Burkinabé",
    "Burundian",
    "Cabo Verdean",
    "Cambodian",
    "Cameroonian",
    "Canadian",
    "Central African",
    "Chadian",
    "Chilean",
    "Chinese",
    "Colombian",
    "Comoran",
    "Congolese",
    "Costa Rican",
    "Croatian",
    "Cuban",
    "Cypriot",
    "Czech",
    "Danish",
    "Djiboutian",
    "Dominican",
    "Ecuadorean",
    "Egyptian",
    "Salvadoran",
    "Salvadorian",
    "Equatorial Guinean",
    "Eritrean",
    "Estonian",
    "Swazi",
    "Ethiopian",
    "Fijian",
    "Finnish",
    "French",
    "Gabonese",
    "Gambian",
    "Georgian",
    "German",
    "Ghanaian",
    "Greek",
    "Grenadian",
    "Guatemalan",
    "Guinean",
    "Guinea-Bissauan",
    "Guyanese",
    "Haitian",
    "Honduran",
    "Hungarian",
    "Icelandic",
    "Indian",
    "Indonesian",
    "Iranian",
    "Iraqi",
    "Irish",
    "Israeli",
    "Italian",
    "Jamaican",
    "Japanese",
    "Jordanian",
    "Kazakhstani",
    "Kenyan",
    "I-Kiribati",
    "North Korean",
    "South Korean",
    "Kosovar",
    "Kuwaiti",
    "Kyrgyz",
    "Laotian",
    "Latvian",
    "Lebanese",
    "Mosotho",
    "Liberian",
    "Libyan",
    "Liechtensteiner",
    "Lithuanian",
    "Luxembourger",
    "Malagasy",
    "Malawian",
    "Malaysian",
    "Maldivian",
    "Malian",
    "Maltese",
    "Marshallese",
    "Mauritanian",
    "Mauritian",
    "Mexican",
    "Micronesian",
    "Moldovan",
    "Monegasque",
    "Mongolian",
    "Montenegrin",
    "Moroccan",
    "Mozambican",
    "Burmese",
    "Namibian",
    "Nauruan",
    "Nepalese",
    "Dutch",
    "New Zealander",
    "Nicaraguan",
    "Nigerien",
    "Nigerian",
    "North Macedonian",
    "Norwegian",
    "Omani",
    "Pakistani",
    "Palauan",
    "Panamanian",
    "Papua New Guinean",
    "Paraguayan",
    "Peruvian",
    "Filipino",
    "Polish",
    "Portuguese",
    "Qatari",
    "Romanian",
    "Russian",
    "Rwandan",
    "Saint Kitts and Nevisian",
    "Saint Lucian",
    "Saint Vincent and the Grenadines",
    "Samoan",
    "San Marinese",
    "Sao Tomean",
    "Saudi Arabian",
    "Senegalese",
    "Serbian",
    "Seychellois",
    "Sierra Leonean",
    "Singaporean",
    "Slovak",
    "Slovenian",
    "Solomon Islander",
    "Somali",
    "South African",
    "South Sudanese",
    "Spanish",
    "Sri Lankan",
    "Sudanese",
    "Surinamese",
    "Swedish",
    "Swiss",
    "Syrian",
    "Taiwanese",
    "Tajik",
    "Tanzanian",
    "Thai",
    "Timorese",
    "Togolese",
    "Tongan",
    "Trinidadian or Tobagonian",
    "Tunisian",
    "Turkish",
    "Turkmen",
    "Tuvaluan",
    "Ugandan",
    "Ukrainian",
    "Emirian",
    "British",
    "American",
    "Uruguayan",
    "Uzbekistani",
    "Ni-Vanuatu",
    "Vatican",
    "Venezuelan",
    "Vietnamese",
    "Yemenite",
    "Zambian",
    "Zimbabwean",
]

# Lists for Western, Educated, Industrialized, Rich and Democratic (WEIRD)
# countries
weird_countries = [
    "United States",
    "USA",
    "Canada",
    "United Kingdom",
    "UK",
    "Ireland",
    "Australia",
    "New Zealand",
    "Germany",
    "France",
    "Netherlands",
    "Belgium",
    "Luxembourg",
    "Switzerland",
    "Austria",
    "Denmark",
    "Norway",
    "Sweden",
    "Finland",
    "Iceland",
]
weird_demonyms = [
    "American",
    "Canadian",
    "British",
    "Irish",
    "Australian",
    "New Zealander",
    "German",
    "French",
    "Dutch",
    "Belgian",
    "Luxembourger",
    "Swiss",
    "Austrian",
    "Danish",
    "Norwegian",
    "Swedish",
    "Finnish",
    "Icelandic",
]

# Lists for non-WEIRD countries
non_weird_countries = [
    country for country in countries if country not in weird_countries
]
non_weird_demonyms = [demonym for demonym in demonyms if demonym not in weird_demonyms]

# Lists for all countries' names stemmed
stemmed = [
    "Afghan*",
    "Alban*",
    "Alger*",
    "Andorr*",
    "Angol*",
    "Antigu* and Barbud*",
    "Argentin*",
    "Armen*",
    "Austral*",
    "Austri*",
    "Azerbaijan*",
    "Baham*",
    "Bahrain*",
    "Banglades*",
    "Barbad*",
    "Belarus*",
    "Belg*",
    "Beliz*",
    "Benin*",
    "Bhutan*",
    "Bolivi*",
    "Bosnia and Herzegovin*",
    "Botswan*",
    "Brazil*",
    "Brune*",
    "Bulgari*",
    "Burkina Fas*",
    "Burund*",
    "Cabo Verde*",
    "Cambodi*",
    "Cameroon*",
    "Canad*",
    "Central African*",
    "Chad*",
    "Chil*",
    "Chin*",
    "Colomb*",
    "Comor*",
    "Cong*",
    "Costa Ric*",
    "Croat*",
    "Cub*",
    "Cypr*",
    "Czech*",
    "Denmark*",
    "Djibout*",
    "Dominic*",
    "Ecuad*",
    "Egypt*",
    "Salvador*",
    "Equatorial Guine*",
    "Eritre*",
    "Eston*",
    "Eswatin*",
    "Ethiopi*",
    "Fij*",
    "Finland*",
    "Franc*",
    "Gabon*",
    "Gambi*",
    "Georg*",
    "German*",
    "Ghan*",
    "Greec*",
    "Grenad*",
    "Guatemal*",
    "Guine*",
    "Guinea-Bissau*",
    "Guyan*",
    "Hait*",
    "Hondur*",
    "Hungar*",
    "Iceland*",
    "Indi*",
    "Indones*",
    "Iran*",
    "Iraq*",
    "Irel*",
    "Isra*",
    "Ital*",
    "Jamaic*",
    "Jap*",
    "Jord*",
    "Kazakhstan*",
    "Keny*",
    "Kiribat*",
    "North Kore*",
    "South Kore*",
    "Kosov*",
    "Kuwait*",
    "Kyrgyzstan*",
    "Laos*",
    "Latvi*",
    "Leban*",
    "Lesoth*",
    "Liber*",
    "Liby*",
    "Liechtenstein*",
    "Lithuani*",
    "Luxembourg*",
    "Madagas*",
    "Malaw*",
    "Malays*",
    "Maldiv*",
    "Mal*",
    "Malt*",
    "Marshall Islands*",
    "Mauritani*",
    "Mauriti*",
    "Mexic*",
    "Micrones*",
    "Moldov*",
    "Monac*",
    "Mongol*",
    "Montenegr*",
    "Morocc*",
    "Mozambiqu*",
    "Myanm*",
    "Namibi*",
    "Naur*",
    "Nep*",
    "Netherland*",
    "New Zealand*",
    "Nicaragu*",
    "Niger*",
    "Nigeri*",
    "North Macedonian*",
    "Norway*",
    "Oman*",
    "Pakist*",
    "Palau*",
    "Panam*",
    "Papua New Guine*",
    "Paraguay*",
    "Per*",
    "Philippin*",
    "Pol*",
    "Portug*",
    "Qatar*",
    "Romani*",
    "Russ*",
    "Rwand*",
    "Saint Kitts and Nevis*",
    "Saint Luci*",
    "Saint Vincent and the Grenadin*",
    "Sam*",
    "San Marin*",
    "Sao Tom* and Principe*",
    "Saudi Arabi*",
    "Seneg*",
    "Serbi*",
    "Seychell*",
    "Sierra Leon*",
    "Singapor*",
    "Slovak*",
    "Sloven*",
    "Solomon Islands*",
    "Somal*",
    "South Afric*",
    "South Sudan*",
    "Spain*",
    "Sri Lank*",
    "Sudan*",
    "Surinam*",
    "Swed*",
    "Switzerland*",
    "Syri*",
    "Taiw*",
    "Tajikistan*",
    "Tanzani*",
    "Thail*",
    "Timor-Lest*",
    "Tog*",
    "Tong*",
    "Trinidad and Tobag*",
    "Tunisi*",
    "Turk*",
    "Turkmenistan*",
    "Tuvalu*",
    "Ugand*",
    "Ukrain*",
    "Emirat*",
    "Brit*",
    "Americ*",
    "Uruguay*",
    "Uzbekistan*",
    "Vanuat*",
    "Vatican*",
    "Venezuel*",
    "Vietnam*",
    "Yemen*",
    "Zambi*",
    "Zimbabw*",
]

# Lists for Latin American and Caribbean (LAC) countries
lac_countries = [
    "Argentina",
    "Bolivia",
    "Brazil",
    "Chile",
    "Colombia",
    "Costa Rica",
    "Cuba",
    "Dominican Republic",
    "Ecuador",
    "El Salvador",
    "Guatemala",
    "Haiti",
    "Honduras",
    "Jamaica",
    "Mexico",
    "Nicaragua",
    "Panama",
    "Paraguay",
    "Peru",
    "Puerto Rico",
    "Uruguay",
    "Venezuela",
]
lac_demonyms = [
    "Argentinian",
    "Argentine",
    "Bolivian",
    "Brazilian",
    "Chilean",
    "Colombian",
    "Costa Rican",
    "Cuban",
    "Dominican",
    "Ecuadorian",
    "Salvadoran",
    "Salvadorian",
    "Guatemalan",
    "Haitian",
    "Honduran",
    "Jamaican",
    "Mexican",
    "Nicaraguan",
    "Panamanian",
    "Paraguayan",
    "Peruvian",
    "Puerto Rican",
    "Uruguayan",
    "Venezuelan",
]

###############################################
import re
import pandas as pd


def language_bias_helper(query: str) -> str:
    """
    Returns a query without the language restriction.
    """
    return re.sub(r"(AND\s)*LANGUAGE\(\w+\)", "", query)


def publication_bias_helper(query: str) -> str:
    """
    Returns a query without the language restriction.
    """
    return re.sub(r"(AND\s)*SRCTYPE\(\w+\)", "", query)


def find_localization_in_text(
    text: str, countries: list[str] = countries, demonyms: list[str] = demonyms
) -> bool:
    """
    Returns True if any country name or demonym is found in the text.
    """
    text_words = text.lower().split()
    if any(location.lower() in text_words for location in countries + demonyms):
        return True
    else:
        return False


def determine_localization_in_title(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add column 'localization_in_title' (boolean)
    """
    df_copy = df.copy()
    df_copy["localization_in_title"] = df["dc:title"].apply(find_localization_in_text)
    return df_copy


###############################################
import json
import pandas as pd

from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch


def get_environment_var(env, fallback):
    try:
        var = os.environ[env]
        if isinstance(fallback, int):
            var = int(var)
    except (KeyError, ValueError):
        if fallback is None:
            # module_logger.error(
            #     f"The required environment variable '{env}' is not set \
            #         and has not got a fallback value.")
            raise
        else:
            var = fallback
    return var


project_dir = get_environment_var("project_dir", None)
scopus_config_file = get_environment_var("scopus_config_file", None)
scopus_data_dir = get_environment_var("scopus_data_dir", None)


con_file = open(scopus_config_file)
config = json.load(con_file)
con_file.close()

# Initialize Elsevier client
client = ElsClient(config["apikey"])

# Define selected columns
selected_columns = [
    "dc:identifier",
    "dc:title",
    "dc:creator",
    "prism:publicationName",
    "prism:coverDate",
    "prism:aggregationType",
    "subtypeDescription",
    "prism:doi",
    "eid",
    "openaccess",
]


# Functions to retrieve results from Scopus API
def scopus_query_list_constructor(
    initial_query: str, long_list: list[str], search_field: str = "ALL", step: int = 20
):
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
            initial_query
            + " AND "
            + search_field
            + "({"
            + "} OR {".join(long_list[i : i + step])
            + "})"
        )
    return list_of_queries


def retrieve_results_from_query(query: str) -> pd.DataFrame:
    """
    Retrieve results from query.
    """
    # module_logger.info(f"Retrieving results from Scopus API for query: {query}")
    # Initialize document search object and execute search
    doc_srch = ElsSearch(query, "scopus")
    doc_srch.execute(client, get_all=True)
    # Retrieve results
    results = doc_srch.results
    # module_logger.info(f"{len(results)} results retrieved from Scopus API.")

    results_df = convert_results_to_dataframe(results)
    if len(results_df) > 0:
        results_df["localization_in_title_abstract_or_key"] = "TITLE-ABS-KEY" in query
    else:
        results_df["localization_in_title_abstract_or_key"] = None
    # module_logger.info("Query results converted to dataframe.")
    return results_df


def retrieve_results_from_list_of_queries(
    list_of_queries: list[str],
    max_date: str,
) -> pd.DataFrame:
    """
    Retrieve results from list of queries and concatenate them.
    """
    # module_logger.info(f"Retrieving results from {len(list_of_queries)} queries.")
    results_dfs = []
    for query in list_of_queries:
        results_df = retrieve_results_from_query(query)
        results_dfs.append(results_df)
    # module_logger.info(f"Concatenating {len(results_dfs)} dataframes.")
    results_df = pd.concat(results_dfs)
    results_df = results_df.drop_duplicates(subset=["dc:identifier"])
    results_df = results_df.reset_index(drop=True)
    # module_logger.info(
    #     f"Deduplicated results in concatenated dataframe: {len(results_df)}"
    # )
    results_df = apply_further_transformations(results_df, max_date=max_date)
    # module_logger.info(f"{len(results_df)} results retrieved from the list of queries.")
    return results_df


# Functions to process imported results
def convert_results_to_dataframe(
    results: list, selected_columns=selected_columns
) -> pd.DataFrame:
    """Convert results to dataframe."""
    # module_logger.info(f"Converting {len(results)} results to dataframe.")
    results_df = pd.DataFrame.from_records(results)
    try:
        results_df = results_df[selected_columns]
        results_df = results_df.drop_duplicates(subset=["dc:identifier"])
        results_df["openaccess"] = results_df["openaccess"].astype(int)
        results_df = results_df.reset_index(drop=True)
        # module_logger.info(
        #     f"Deduplicated results stored in dataframe: {len(results_df)}"
        # )
    except KeyError:
        # module_logger.info(f"Columns not converted to dataframe: {results_df.columns})")
        results_df = pd.DataFrame(columns=selected_columns)
    # module_logger.info(f"{len(results_df)} results converted to dataframe.")
    return results_df


def apply_further_transformations(
    df: pd.DataFrame,
    max_date: str = None,
) -> pd.DataFrame:
    """
    Apply further transformations to dataframe:
    - add column 'localization_in_title' (boolean)
    - filter by max_date
    - drop duplicates
    - reset index
    """
    # module_logger.info("Applying further transformations to dataframe.")
    df_copy = df.copy()
    df_copy = determine_localization_in_title(df_copy)
    if max_date:
        # module_logger.info(f"Filtering by max_date: {max_date}")
        df_copy = df_copy[df_copy["prism:coverDate"] < max_date]
        # module_logger.info(f"{len(df_copy)} results after filtering by max_date.")
    df_copy.drop_duplicates(subset=["dc:identifier"], inplace=True)
    # module_logger.info(f"{len(df_copy)} results after deduplication.")
    df_copy.reset_index(drop=True, inplace=True)
    # module_logger.info("Further transformations applied to dataframe.")
    return df_copy


###############################################

mergoni_2021_scopus_query = (
    "ALL({data envelopment analysis})"
    + " AND ALL({policy evaluation})"
    + " AND PUBYEAR > 1956"
    + " AND PUBYEAR < 2022"
    + " AND LANGUAGE(english)"
    + " AND SRCTYPE(j)"
)
max_date = "2021-02-01"

###############################################

st.write("Unbiased Request - SCOPUS")

if st.checkbox("Load example query"):
    st.session_state.original_query = mergoni_2021_scopus_query
    st.session_state.max_date = max_date

# st.session_state.original_query = ""
# st.session_state.max_date = ""

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


if st.checkbox("Retrieve data from your original query and load it into cache"):
    data_load_state = st.text("Loading data for your query...")
    data_original = load_data(
        st.session_state.original_query, st.session_state.max_date
    )
    data_load_state.text(f"Data loaded! Retrieved {len(data_original)} results.")

    if st.checkbox("Show original data head"):
        st.subheader("Original query data head")
        st.write(data_original.head(5))

st.session_state.lang_bias_query = language_bias_helper(st.session_state.original_query)
st.session_state.pub_bias_query = publication_bias_helper(
    st.session_state.original_query
)

st.write("This is your query without language bias:")
st.session_state.lang_bias_query

if st.checkbox("Retrieve data from your query without language bias"):
    data_load_state = st.text("Loading data for your query...")
    data_lang = load_data(st.session_state.lang_bias_query, st.session_state.max_date)
    data_load_state.text(f"Data loaded! Retrieved {len(data_lang)} results.")

    if st.checkbox("Show language helper data head"):
        st.subheader("Language helper query data head")
        st.write(data_lang.head(5))

st.write("This is your query without publication bias:")
st.session_state.pub_bias_query

if st.checkbox("Retrieve data from your query without publication bias"):
    data_load_state = st.text("Loading data for your query...")
    data_pub = load_data(st.session_state.pub_bias_query, st.session_state.max_date)
    data_load_state.text(f"Data loaded! Retrieved {len(data_pub)} results.")

    if st.checkbox("Show publication helper data head"):
        st.subheader("Publication helper query data head")
        st.write(data_pub.head(5))
