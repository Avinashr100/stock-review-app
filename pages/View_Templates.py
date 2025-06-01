import streamlit as st
import os
import json

TEMPLATE_DIR = "templates"
os.makedirs(TEMPLATE_DIR, exist_ok=True)

st.title("🔍 View Saved Templates")

search_term = st.text_input("Search by Stock Name")

template_files = sorted([f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".json")])

if search_term:
    template_files = [f for f in template_files if search_term.lower() in f.lower()]

if template_files:
    for filename in template_files:
        stock_name = filename.replace(".json", "")
        filepath = os.path.join(TEMPLATE_DIR, filename)
        with open(filepath, "r") as f:
            data = json.load(f)

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
    st.info("No templates found. Create a new one first.")
