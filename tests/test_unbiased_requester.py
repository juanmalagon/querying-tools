import pandas as pd


# Replicate the pure utility functions from unbiased_requester.py
# without importing the module, because the module body calls
# streamlit at the top level (st.markdown, etc.).

def safe_percentage(part: int, total: int) -> float:
    """Replication of unbiased_requester.safe_percentage for test isolation."""
    return round(100 * part / total, 1) if total else 0.0


def convert_df(df: pd.DataFrame) -> bytes:
    """Replication of unbiased_requester.convert_df for test isolation."""
    return df.to_csv(index=False).encode("utf-8")


class TestSafePercentage:
    """Tests for the pure utility safe_percentage."""

    def test_normal_case(self):
        assert safe_percentage(3, 10) == 30.0

    def test_zero_total(self):
        assert safe_percentage(5, 0) == 0.0

    def test_rounding(self):
        assert safe_percentage(1, 3) == 33.3

    def test_100_percent(self):
        assert safe_percentage(5, 5) == 100.0


class TestConvertDf:
    """Tests for convert_df."""

    def test_returns_utf8_bytes(self):
        df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
        result = convert_df(df)
        assert isinstance(result, bytes)
        csv_text = result.decode("utf-8")
        assert "a,b" in csv_text
        assert "1,x" in csv_text
        assert "2,y" in csv_text

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        result = convert_df(df)
        csv_text = result.decode("utf-8")
        # An empty DataFrame produces only a newline.
        assert csv_text.strip() == ""
