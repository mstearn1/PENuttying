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
