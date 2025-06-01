import streamlit as st
import os
import json

TEMPLATE_DIR = "templates"
os.makedirs(TEMPLATE_DIR, exist_ok=True)
PASSWORD = "Changed@123"

st.title("📝 Create/Edit Stock Template")

# Load stock name from session or prompt input
if "stock_name" in st.session_state and st.session_state.stock_name:
    stock_name = st.session_state.stock_name
    st.text_input("Stock Name", value=stock_name, disabled=True, key="existing_stock")
else:
    stock_name = st.text_input("Enter Stock Name", key="new_stock")

if stock_name:
    file_path = os.path.join(TEMPLATE_DIR, f"{stock_name}.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = {}

    signed_off = data.get("signed_off", False)
    revision = data.get("revision", 0)

    # Unlock section
    if signed_off and not st.session_state.get("unlocked", False):
        st.warning("🔒 This template is signed off. Enter password to edit.")
        password = st.text_input("Enter password", type="password", key="unlock_password")
        if st.button("🔓 Unlock Template"):
            if password == PASSWORD:
                st.session_state.unlocked = True
                st.success("Unlocked for editing.")
            else:
                st.error("Incorrect password.")

    is_locked = signed_off and not st.session_state.get("unlocked", False)

    with st.form("template_form"):
        data["company_description"] = st.text_area("What does the company do?", value=data.get("company_description", ""), disabled=is_locked)
        data["financial_stability"] = st.text_area("Is the company financially stable?", value=data.get("financial_stability", ""), disabled=is_locked)
        data["competitive_advantage"] = st.text_area("What is its USP?", value=data.get("competitive_advantage", ""), disabled=is_locked)
        data["reason_for_sale"] = st.text_area("Reason for Sale", value=data.get("reason_for_sale", ""), disabled=is_locked)
        data["repurchase_future"] = st.text_input("Will you repurchase in future?", value=data.get("repurchase_future", ""), disabled=is_locked)

        submitted = st.form_submit_button("💾 Save Template")
        if submitted and not is_locked:
            revision += 1
            data["revision"] = revision
            data["signed_off"] = False
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            st.success("Template saved.")

    if not is_locked:
        if st.button("🔒 Sign Off"):
            data["signed_off"] = True
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            st.success("Template signed off.")
else:
    st.info("Please enter a stock name to begin.")
