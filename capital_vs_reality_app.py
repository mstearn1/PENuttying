import streamlit as st
import numpy as np
import pandas as pd

# Optional: safely try importing matplotlib for local dev environments
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    plotting_available = True
except ModuleNotFoundError:
    plotting_available = False

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

# CPG Investment Analyzer
elif module == "CPG Investment Analyzer":
    st.header("🧃 CPG Investment Analyzer – Path to Success or Failure")
    gross_margin = st.slider("Gross Margin at Launch (%)", 10, 90, 45)
    channel = st.selectbox("Primary Sales Channel", ["DTC", "Retail", "Amazon", "Hybrid"])
    brand_strength = st.select_slider("Brand Strength", ["Weak", "Average", "Strong", "Celebrity"])
    sku_count = st.slider("Number of SKUs", 1, 50, 10)
    simulate_failure = st.checkbox("Simulate Operational Failure")

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

    st.metric("Survival Score", f"{score:.1f}")
    st.subheader(f"Outcome: {status}")

    # Optional plotting only if available
    if plotting_available:
        st.subheader("📊 Score Benchmark (Simulated)")
        np.random.seed(42)
        sim_scores = np.random.normal(loc=50, scale=15, size=1000)
        import matplotlib.pyplot as plt
        import seaborn as sns
        fig, ax = plt.subplots()
        sns.histplot(sim_scores, bins=30, color='skyblue', kde=True, ax=ax)
        ax.axvline(score, color='red', linestyle='--', label='Your Score')
        ax.set_title("Simulated Score Distribution")
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("Plotting not available in this environment. Please install matplotlib and seaborn locally to enable visuals.")
