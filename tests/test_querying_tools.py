from resources.querying_tools import language_bias_tool, publication_bias_tool


def test_language_bias_tool_removes_language_filter():
    query = "ALL({education}) AND LANGUAGE(english) AND SRCTYPE(j)"

    result = language_bias_tool(query)

    assert "LANGUAGE(english)" not in result
    assert "SRCTYPE(j)" in result


def test_publication_bias_tool_removes_source_type_filter():
    query = "ALL({education}) AND LANGUAGE(english) AND SRCTYPE(j)"

    result = publication_bias_tool(query)

    assert "SRCTYPE(j)" not in result
    assert "LANGUAGE(english)" in result
