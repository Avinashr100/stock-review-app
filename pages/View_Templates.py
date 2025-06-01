import streamlit as st
from firebase_utils import list_all_templates
from firebase_loader import init_firebase

init_firebase()
st.title("🔍 View Saved Templates")

search_term = st.text_input("Search by Stock Name")
templates = list_all_templates()

if templates:
    for stock_name, data in templates.items():
        if search_term.lower() in stock_name.lower():
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"**{stock_name}**")
                st.write(f"Revision: {data.get('revision', 0)} | Signed Off: {'✅' if data.get('signed_off') else '❌'}")
            with col2:
                if st.button("Open", key=stock_name):
                    st.session_state.stock_name = stock_name
                    st.session_state.unlocked = False
                    st.switch_page("pages/Create_Template.py")
else:
    st.info("No templates found.")
