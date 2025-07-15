# pages/page_3_Visualization.py

import streamlit as st
import uuid
import os
from modules.visualization import generate_bias_visualizations
from modules.sidebar import render_sidebar  # 👈 Add this

st.set_page_config(page_title="📊 Step 3: Visualize Bias Trends", layout="wide")

render_sidebar()  # 👈 And call this

# ============ Header ============
st.markdown("<h1 style='color:#e63946;'>📊 Step 3: Visualize Bias Trends</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#adb5bd;'>Upload your annotated script CSV to generate saved visual summaries of gendered stereotype distribution.</p>", unsafe_allow_html=True)

# ============ File Upload ============
uploaded_csv = st.file_uploader("📄 Upload annotated script CSV", type=["csv"])

if uploaded_csv:
    try:
        base_id = uploaded_csv.name.rsplit(".", 1)[0] + "_" + uuid.uuid4().hex[:6]
        saved_csv_path = f"data/{base_id}.csv"
        with open(saved_csv_path, "wb") as f:
            f.write(uploaded_csv.read())

        overall_csv_path, gender_csv_path, plot_path = generate_bias_visualizations(saved_csv_path, output_dir="data")

        st.image(plot_path, caption="Overall Stereotype Distribution", use_container_width=True)

        with open(overall_csv_path, "rb") as f1:
            st.download_button(
                "📥 Download Overall Scores CSV",
                f1,
                file_name=os.path.basename(overall_csv_path),
                mime="text/csv"
            )

        with open(gender_csv_path, "rb") as f2:
            st.download_button(
                "📥 Download Gender-wise Scores CSV",
                f2,
                file_name=os.path.basename(gender_csv_path),
                mime="text/csv"
            )

        st.success("✅ All files saved to the /data folder!")

    except Exception as e:
        st.error(f"❌ Error generating plots: {e}")
