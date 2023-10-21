import streamlit as st

st.write("Unbiased Request - SCOPUS")

st.text_input("Insert your original query", key="original_query")

st.write("Unbiased query:")
st.session_state.original_query
