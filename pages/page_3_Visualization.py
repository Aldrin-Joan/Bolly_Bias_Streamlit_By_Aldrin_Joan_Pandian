# pages/page_3_Visualization.py

import streamlit as st
import os
import uuid
from modules.visualization import generate_bias_visualizations

st.set_page_config(page_title="Bias Visualization", layout="wide")
st.title("📊 Step 3: Visualize Bias Trends")

uploaded_csv = st.file_uploader("📄 Upload annotated script CSV", type=["csv"])

if uploaded_csv:
    # Extract base name (without extension)
    original_name = uploaded_csv.name.replace(".csv", "").replace(".CSV", "")
    base_id = original_name + "_" + uuid.uuid4().hex[:6]  # Optional for uniqueness

    saved_csv_path = f"data/{base_id}.csv"
    with open(saved_csv_path, "wb") as f:
        f.write(uploaded_csv.read())

    try:
        overall_csv, gender_csv, plot_path = generate_bias_visualizations(saved_csv_path, output_dir="data")

        st.success("✅ Visualization generated successfully.")
        st.image(plot_path, caption="Overall Stereotype Distribution", use_container_width=True)

        with open(overall_csv, "rb") as f1:
            st.download_button(
                "📥 Download Overall Scores CSV",
                f1,
                file_name=f"{base_id}_bias_scores_overall.csv"
            )

        with open(gender_csv, "rb") as f2:
            st.download_button(
                "📥 Download Gender-wise Scores CSV",
                f2,
                file_name=f"{base_id}_bias_scores_by_gender.csv"
            )

    except Exception as e:
        st.error(f"❌ Error: {e}")
