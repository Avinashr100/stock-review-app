import streamlit as st

st.set_page_config(page_title="Stock Review Dashboard")

st.title("📊 Stock Review App")

st.write("Click a button below to continue.")

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Create New Template"):
        st.session_state.stock_name = ""
        st.query_params.update(new="1")
        st.switch_page("pages/Create_Template.py")

with col2:
    if st.button("🔍 View Saved Templates"):
        st.switch_page("pages/View_Templates.py")
