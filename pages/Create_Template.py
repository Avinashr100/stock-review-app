
import streamlit as st
import os
import json

TEMPLATE_DIR = "templates"
os.makedirs(TEMPLATE_DIR, exist_ok=True)

PASSWORD = "Changed@123"

# Detect fresh creation
query_params = st.query_params
is_new = query_params.get("new") == "1"

if is_new:
    st.session_state.clear()

st.title("📝 Create Stock Review Template")


if "stock_name" in st.session_state and st.session_state.stock_name:
    stock_name = st.session_state.stock_name
    st.text_input("Stock Name (locked)", value=stock_name, disabled=True)
else:
    stock_name = st.text_input("Enter Stock Name (This will be the file name)", key="stock_name")


if stock_name:
    file_path = os.path.join(TEMPLATE_DIR, f"{stock_name}.json")

    # Load or initialize data
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        revision = data.get("revision", 0)
        signed_off = data.get("signed_off", False)
    else:
        data = {}
        revision = 0
        signed_off = False

    # Handle sign-off lock
    
    if signed_off and not st.session_state.get("unlocked", False) and st.session_state.get("stock_name") == stock_name:
        st.warning("🔒 This template is signed off. Viewing is allowed. To edit, enter password below.")
        password_input = st.text_input("Enter password to unlock for editing", type="password")
        if password_input == PASSWORD:
            st.session_state.unlocked = True
            st.success("Template unlocked for editing.")

        st.warning("🔒 This template is signed off and locked.")
        password_input = st.text_input("Enter password to unlock for editing", type="password")
        if password_input == PASSWORD:
            st.session_state.unlocked = True
            st.success("Template unlocked.")
        else:
            st.stop()

    # Form
    with st.form("template_form"):
        st.subheader("Company Fundamentals")
        data["company_description"] = st.text_area("What does the company do, and how does it make money?", value=data.get("company_description", ""))
        data["financial_stability"] = st.text_area("Is the company financially stable?", value=data.get("financial_stability", ""))
        data["competitive_advantage"] = st.text_area("What is the company's competitive advantage or USP?", value=data.get("competitive_advantage", ""))
        data["management_team"] = st.text_area("How experienced and reliable is the management team?", value=data.get("management_team", ""))
        data["growth_history"] = st.text_area("Does the company have a history of consistent growth?", value=data.get("growth_history", ""))

        st.subheader("Stock Performance & Valuation")
        data["valuation"] = {
            "PE Ratio": st.text_input("P/E Ratio", value=data.get("valuation", {}).get("PE Ratio", "")),
            "ROE": st.text_input("ROE", value=data.get("valuation", {}).get("ROE", "")),
            "ROCE": st.text_input("ROCE", value=data.get("valuation", {}).get("ROCE", "")),
            "Sales Growth 5Y": st.text_input("Sales Growth (5Y)", value=data.get("valuation", {}).get("Sales Growth 5Y", "")),
            "Profit Growth 5Y": st.text_input("Profit Growth (5Y)", value=data.get("valuation", {}).get("Profit Growth 5Y", "")),
            "EPS Growth 5Y": st.text_input("EPS Growth (5Y)", value=data.get("valuation", {}).get("EPS Growth 5Y", "")),
            "PEG Ratio": st.text_input("PEG Ratio", value=data.get("valuation", {}).get("PEG Ratio", "")),
            "Shareholder Growth": st.text_input("Shareholder Growth", value=data.get("valuation", {}).get("Shareholder Growth", "")),
        }
        data["stock_performance"] = st.text_area("How has the stock performed in the past five years?", value=data.get("stock_performance", ""))
        data["industry_comparison"] = st.text_area("How does the stock compare to competitors?", value=data.get("industry_comparison", ""))
        data["dividends"] = st.text_area("Does the company pay dividends?", value=data.get("dividends", ""))
        data["price_range"] = st.text_area("52-week high/low & current price", value=data.get("price_range", ""))

        st.subheader("Industry & Market Trends")
        data["industry_performance"] = st.text_area("How is the overall industry performing?", value=data.get("industry_performance", ""))
        data["industry_risks"] = st.text_area("Risks or opportunities in the industry?", value=data.get("industry_risks", ""))
        data["competitor_behavior"] = st.text_area("What are competitors doing differently?", value=data.get("competitor_behavior", ""))
        data["innovation"] = st.text_area("Does the company innovate and adapt?", value=data.get("innovation", ""))
        data["macro_factors"] = st.text_area("Impact of macro factors like inflation", value=data.get("macro_factors", ""))

        st.subheader("Risk Assessment")
        data["major_risks"] = st.text_area("What are the major risks?", value=data.get("major_risks", ""))
        data["volatility"] = st.text_area("How volatile is the stock?", value=data.get("volatility", ""))
        data["regulatory_concerns"] = st.text_area("Any regulatory or legal concerns?", value=data.get("regulatory_concerns", ""))
        data["external_factors"] = st.text_area("External factors affecting company", value=data.get("external_factors", ""))
        data["worst_case"] = st.text_area("Worst-case scenario", value=data.get("worst_case", ""))

        
        data["reason_for_sale"] = st.text_area("Reason for Sale", value=data.get("reason_for_sale", ""))
        data["repurchase_future"] = st.text_input("Will this be repurchased in future?", value=data.get("repurchase_future", ""))
        uploaded_file = st.file_uploader("Upload working Excel file", type=["xlsx", "xls"])

        if uploaded_file:
            data["uploaded_file_name"] = uploaded_file.name

        submitted = st.form_submit_button("💾 Save Template")
        if submitted:
            revision += 1
            data["revision"] = revision
            data["signed_off"] = False
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            st.success("Template saved")

    if not signed_off:
        if st.button("🔒 Sign Off Template"):
            data["signed_off"] = True
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            st.success("Template signed off and locked.")
    else:
        st.info("Template is signed off and locked.")

    st.markdown(f"**Revision Count:** {revision}")
