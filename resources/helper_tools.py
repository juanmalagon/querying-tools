import re
import pandas as pd
from resources.country_lists import (
    countries,
    demonyms,
)


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
    if any(location.lower() in text_words for location in countries+demonyms):
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
    df_copy["localization_in_title"] = df["dc:title"].apply(
        find_localization_in_text)
    return df_copy
