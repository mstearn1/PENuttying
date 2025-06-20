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
    distribution_points = st.number_input("Number of Distribution Points", value=100)
    avg_price = st.number_input("Average Product Price ($)", value=25.0)
    monthly_customers = st.number_input("Monthly Active Customers", value=10000)
    cac = st.number_input("Customer Acquisition Cost ($)", value=30.0)
    conversion_rate = st.slider("Conversion Rate (%)", 0.1, 10.0, 2.0)
    churn_rate = st.slider("Monthly Churn Rate (%)", 0.0, 20.0, 5.0)
    fixed_burn = st.number_input("Monthly Fixed Cash Burn ($)", value=100000.0)
    variable_burn_per_customer = st.number_input("Variable Burn per Customer ($)", value=5.0)
    slotting_fee = st.number_input("Slotting Fee (One-Time Sunk Cost) ($)", value=50000.0)
    optimism_bias = st.checkbox("Include Overconfidence Bias", value=True)

    potential_customers = (tam * 1000) / cac * (conversion_rate / 100)
    churn_adjustment = potential_customers * (churn_rate / 100)
    forecast_customers = potential_customers - churn_adjustment

    if optimism_bias:
        forecast_customers *= 1.2

    forecast_revenue = forecast_customers * avg_price
    revenue_per_point = forecast_revenue / distribution_points if distribution_points else 0
    weekly_sales_per_point = (forecast_revenue / 4) / distribution_points if distribution_points else 0

    variable_burn = forecast_customers * variable_burn_per_customer
    total_burn = fixed_burn + variable_burn
    breakeven_diff = forecast_revenue - total_burn

    st.metric("Forecasted Active Customers", f"{forecast_customers:,.0f}")
    st.metric("Forecasted Monthly Revenue", f"${forecast_revenue:,.0f}")
    st.metric("Revenue per Distribution Point", f"${revenue_per_point:,.2f}")
    st.metric("Weekly Sales per Unit (per Distribution Point)", f"${weekly_sales_per_point:,.2f}")
    st.metric("Total Monthly Cash Burn", f"${total_burn:,.0f}")
    st.metric("Slotting Fee (One-Time)", f"${slotting_fee:,.0f}")

    if breakeven_diff >= 0:
        st.success(f"✅ Monthly Breakeven Achieved with ${breakeven_diff:,.0f} Surplus")
    else:
        st.error(f"❌ Monthly Breakeven Missed by ${abs(breakeven_diff):,.0f}")

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
