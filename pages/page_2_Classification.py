# pages/page_2_Classification.py

import streamlit as st
import pandas as pd
from tqdm import tqdm
from io import BytesIO
from modules.classification import classify_stereotype
from config import load_model_tokenizer
from modules.sidebar import render_sidebar  # ✅ Reusable sidebar

# ============ Page Config ============
st.set_page_config(
    page_title="🎭 Step 2: Bias Classification",
    page_icon="🧠",
    layout="wide",
)

# ============ Hide Default Sidebar ============
hide_sidebar_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="stSidebar"] {
            background-color: #111827;
            padding: 1rem;
            width: 240px;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# ============ Custom Sidebar ============
with st.sidebar:
    render_sidebar()

# ============ Page Header ============
st.markdown("""
    <h1 style='color:#e63946;'>🧠 Step 2: Bias Classification</h1>
    <p style='color:#adb5bd; font-size:16px;'>
        Upload the cleaned script CSV (from Step 1). This module uses a local <b>Mistral-7B</b> LLM to classify each dialogue into one of 14 gender stereotype categories.
    </p>
    <hr style='border:1px solid #444;'/>
""", unsafe_allow_html=True)

# ============ File Upload ============
uploaded_file = st.file_uploader("📤 Upload Cleaned Script CSV", type=["csv"])

if uploaded_file:
    original_name = uploaded_file.name.rsplit(".", 1)[0]
    output_filename = f"{original_name}_classified.csv"

    # 🧾 Preview uploaded file
    df = pd.read_csv(uploaded_file)
    st.write("✅ Uploaded Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # 🚀 Load LLM model
    with st.spinner("🔁 Loading Mistral model..."):
        tokenizer, model = load_model_tokenizer()

    # 🧠 Classify bias
    with st.spinner("🔍 Running gender stereotype classification..."):
        tqdm.pandas()
        df["stereotype_type"] = df["line"].progress_apply(
            lambda line: classify_stereotype(line, tokenizer, model)
        )

    # ✅ Show classified results
    st.success("✅ Classification complete!")
    st.dataframe(df.head(10), use_container_width=True)

    # 📥 Download output
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Classified CSV",
        data=csv_bytes,
        file_name=output_filename,
        mime="text/csv"
    )
else:
    st.info("📎 Please upload a CSV file generated from Step 1.")
