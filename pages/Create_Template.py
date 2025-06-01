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

    def field(label, key, input_type='text', options=None):
        prefix = '✅ ' if signed_off else ''
        full_label = f"{prefix}{label}"
        if input_type == 'textarea':
            return st.text_area(full_label, value=data.get(key, ""), key=key, disabled=is_locked)
        elif input_type == 'select':
            return st.selectbox(full_label, options, index=options.index(data.get(key, options[0])) if data.get(key) in options else 0, key=key, disabled=is_locked)
        else:
            return st.text_input(full_label, value=data.get(key, ""), key=key, disabled=is_locked)

    with st.form("template_form"):
        st.subheader("📘 Company Fundamentals")
        data["company_description"] = field("What does the company do, and how does it make money?", "company_description", 'textarea')
        data["financial_stability"] = field("Is the company financially stable?", "financial_stability", 'textarea')
        data["competitive_advantage"] = field("What is the company's competitive advantage or unique selling point?", "competitive_advantage", 'textarea')
        data["management_team"] = field("How experienced and reliable is the management team?", "management_team", 'textarea')
        data["growth_history"] = field("Does the company have a history of consistent growth in earnings and revenue?", "growth_history", 'textarea')

        st.subheader("📊 Stock Performance & Valuation")
        data["valuation_pe"] = field("P/E Ratio", "valuation_pe")
        data["valuation_roe"] = field("ROE", "valuation_roe")
        data["valuation_roce"] = field("ROCE", "valuation_roce")
        data["valuation_sales"] = field("5 Years Sales Growth", "valuation_sales")
        data["valuation_profit"] = field("5 Years Profit Growth", "valuation_profit")
        data["valuation_eps"] = field("5 Years EPS Growth", "valuation_eps")
        data["valuation_peg"] = field("PEG Ratio", "valuation_peg")
        data["valuation_shareholder"] = field("Shareholder Growth", "valuation_shareholder")
        data["stock_performance"] = field("How has the stock performed in the past five years?", "stock_performance", 'textarea')
        data["industry_comparison"] = field("How does the stock compare to competitors in the same industry?", "industry_comparison", 'textarea')
        data["dividends"] = field("Does the company pay dividends? If yes, how stable are they?", "dividends", 'textarea')
        data["price_range"] = field("What is the stock’s 52-week high and low? Is it trading at a reasonable price now?", "price_range", 'textarea')

        st.subheader("🌍 Industry & Market Trends")
        data["industry_performance"] = field("How is the overall industry performing? Is it growing or declining?", "industry_performance", 'textarea')
        data["industry_risks"] = field("Are there potential risks or opportunities in the industry?", "industry_risks", 'textarea')
        data["competitor_behavior"] = field("What are competitors doing differently? Are they gaining or losing market share?", "competitor_behavior", 'textarea')
        data["innovation"] = field("Does the company innovate and adapt to market changes?", "innovation", 'textarea')
        data["macro_factors"] = field("How does inflation, interest rates, or global events impact this sector?", "macro_factors", 'textarea')

        st.subheader("⚠️ Risk Assessment")
        data["major_risks"] = field("What are the major risks associated with investing in this stock?", "major_risks", 'textarea')
        data["volatility"] = field("How volatile is the stock? Can you handle the ups and downs?", "volatility", 'textarea')
        data["regulatory_concerns"] = field("Are there any regulatory or legal concerns affecting the company?", "regulatory_concerns", 'textarea')
        data["external_factors"] = field("Are there external factors that could hurt the company?", "external_factors", 'textarea')
        data["worst_case"] = field("What’s the worst-case scenario if this stock underperforms?", "worst_case", 'textarea')

        st.subheader("📄 Additional Info")
        data["reason_for_sale"] = field("Reason for Sale", "reason_for_sale", 'textarea')
        data["repurchase_future"] = field("Will you repurchase in future?", "repurchase_future")

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
