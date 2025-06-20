import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit page configuration
st.set_page_config(page_title="CPG Investment Analyzer", layout="wide")
st.title("🧃 CPG Investment Analyzer – Predictive Success Dashboard")

# Sidebar Inputs
st.sidebar.header("🔧 Input Your Brand's Parameters")

gross_margin = st.sidebar.slider("Gross Margin at Launch (%)", 10, 90, 45)
sku_count = st.sidebar.slider("Number of SKUs", 1, 50, 10)
brand_strength_label = st.sidebar.selectbox("Brand Strength", ["Weak", "Average", "Strong", "Celebrity"])
ops_failure = st.sidebar.checkbox("Simulate Operational Failure", value=False)
cash_burn = st.sidebar.number_input("Monthly Cash Burn ($K)", min_value=10, max_value=2000, value=250)
runway_months = st.sidebar.number_input("Cash Runway (Months)", min_value=1, max_value=60, value=12)

# Convert brand strength label to numerical score
brand_strength_scores = {"Weak": 10, "Average": 20, "Strong": 30, "Celebrity": 40}
brand_strength = brand_strength_scores.get(brand_strength_label, 20)

# Calculate survival score
survival_score = gross_margin + brand_strength - (sku_count * 0.5) - (20 if ops_failure else 0)
burn_risk = (cash_burn / 1000) * (12 / max(runway_months, 1))
survival_score -= min(burn_risk * 2, 20)

# Determine outcome based on survival score
if survival_score >= 60:
    status = "✅ Likely to Succeed"
elif survival_score >= 40:
    status = "⚠️ At Risk – Monitor Closely"
else:
    status = "❌ Likely to Fail"

# Display Metrics
st.subheader("📊 Investment Success Prediction")
st.metric("Survival Score", f"{survival_score:.1f}", help="Score factoring margin, brand, SKUs, ops, and cash dynamics")
st.subheader(f"Outcome: {status}")

# Simulate Benchmark Dataset
np.random.seed(42)
n_samples = 1000
gross_margins = np.random.uniform(20, 80, n_samples)
sku_counts = np.random.randint(1, 50, n_samples)
brand_strength_scores_data = np.random.choice([10, 20, 30, 40], n_samples)
ops_failures = np.random.binomial(1, 0.2, n_samples)
cash_burns = np.random.uniform(100, 1500, n_samples)
runways = np.random.uniform(3, 24, n_samples)

burn_risks = (cash_burns / 1000) * (12 / runways)
survival_scores = gross_margins + brand_strength_scores_data - (sku_counts * 0.5) - (ops_failures * 20) - np.minimum(burn_risks * 2, 20)
outcomes = np.where(survival_scores >= 60, "Likely to Succeed", np.where(survival_scores >= 40, "At Risk", "Likely to Fail"))

benchmark_df = pd.DataFrame({
    "Gross Margin": gross_margins,
    "SKU Count": sku_counts,
    "Brand Strength": brand_strength_scores_data,
    "Ops Failure": ops_failures,
    "Cash Burn ($K)": cash_burns,
    "Runway (mo)": runways,
    "Survival Score": survival_scores,
    "Outcome": outcomes
})

# Create Benchmark Plot
st.subheader("📈 Benchmark Comparison")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=benchmark_df, x="Survival Score", hue="Outcome", multiple="stack", bins=30, palette="Set2", ax=ax)
ax.axvline(survival_score, color='black', linestyle='--', label='Your Score')
ax.legend()
ax.set_title("Survival Score Distribution with Your Brand Overlay")
st.pyplot(fig)

st.write("\n\n📌 **Interpretation Tip:** If your score is left of the majority 'Success' cluster, reevaluate your burn, SKU strategy, or ops reliability.")
