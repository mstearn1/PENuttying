import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Capital vs Reality Interactive Model", layout="wide")
st.title("Capital vs Reality: Interactive Diagnostic Engine")

# Sidebar for module selection
st.sidebar.title("Explore Modules")
module = st.sidebar.radio("Select Module", ["Talent Pipeline Simulator", "Forecasting Engine", "CPG Investment Analyzer"])

# Talent Pipeline Simulator
if module == "Talent Pipeline Simulator":
    st.header("🧠 Talent Pipeline Simulator – PE/IB Recruitment and Performance")
    ivy_pct = st.slider("Percent of Hires from Ivy League", 0, 100, 80)
    ops_exp_pct = st.slider("Percent of Hires with Ops Experience", 0, 100, 10)
    conversion_rate = st.slider("Analyst-to-Associate Conversion Rate (%)", 0, 100, 60)
    embed_ops_partner = st.checkbox("Embed Operating Partner in Deal Teams", value=False)

    irr_base = 12
    irr = irr_base + (ops_exp_pct * 0.05) - ((ivy_pct - 50) * 0.02)
    if embed_ops_partner:
        irr += 3

    st.metric("Estimated Fund IRR", f"{irr:.2f}%")

# Forecasting Engine
elif module == "Forecasting Engine":
    st.header("📈 Forecasting Engine – Building and Breaking Models")
    tam = st.number_input("Total Addressable Market ($M)", value=500)
    cac = st.number_input("Customer Acquisition Cost ($)", value=30.0)
    conversion_rate = st.slider("Conversion Rate (%)", 0.1, 10.0, 2.0)
    churn_rate = st.slider("Monthly Churn Rate (%)", 0.0, 20.0, 5.0)
    optimism_bias = st.checkbox("Include Overconfidence Bias", value=True)

    base_customers = (tam * 1000) / cac * (conversion_rate / 100)
    churn_adjustment = base_customers * (churn_rate / 100)
    forecast_customers = base_customers - churn_adjustment

    if optimism_bias:
        forecast_customers *= 1.2

    st.metric("Forecasted Active Customers", f"{forecast_customers:,.0f}")

# CPG Investment Analyzer with Multi-Brand Comparison
elif module == "CPG Investment Analyzer":
    st.header("🧃 CPG Investment Analyzer – Path to Success or Failure")

    st.subheader("Enter Brand Data")
    num_brands = st.number_input("How many brands do you want to compare?", min_value=1, max_value=5, value=1)

    all_results = []

    for i in range(num_brands):
        st.markdown(f"### Brand {i+1}")
        gross_margin = st.slider(f"Gross Margin at Launch (%) – Brand {i+1}", 10, 90, 45, key=f"gm_{i}")
        channel = st.selectbox(f"Primary Sales Channel – Brand {i+1}", ["DTC", "Retail", "Amazon", "Hybrid"], key=f"channel_{i}")
        brand_strength = st.select_slider(f"Brand Strength – Brand {i+1}", ["Weak", "Average", "Strong", "Celebrity"], key=f"strength_{i}")
        sku_count = st.slider(f"Number of SKUs – Brand {i+1}", 1, 50, 10, key=f"sku_{i}")
        simulate_failure = st.checkbox(f"Simulate Operational Failure – Brand {i+1}", key=f"fail_{i}")

        score = gross_margin + (10 if brand_strength == "Strong" else 20 if brand_strength == "Celebrity" else 0)
        score -= sku_count * 0.5
        if simulate_failure:
            score -= 20

        if score >= 60:
            status = "✅ Likely to Succeed"
        elif score >= 40:
            status = "⚠️ At Risk – Monitor Closely"
        else:
            status = "❌ Likely to Fail"

        all_results.append({
            "Brand": f"Brand {i+1}",
            "Survival Score": round(score, 1),
            "Outcome": status
        })

    result_df = pd.DataFrame(all_results)
    st.subheader("📋 Multi-Brand Results")
    st.dataframe(result_df.set_index("Brand"))

    st.subheader("📊 Outcome Distribution")
    outcome_counts = result_df["Outcome"].value_counts().reset_index()
    outcome_counts.columns = ["Outcome", "Count"]
    st.bar_chart(outcome_counts.set_index("Outcome"))
