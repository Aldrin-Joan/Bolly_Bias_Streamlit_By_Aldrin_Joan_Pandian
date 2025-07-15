# pages/page_1_data_cleaning.py

import streamlit as st
import pandas as pd
from modules.data_cleaning import process_pdf
from modules.sidebar import render_sidebar  # ✅ Reusable sidebar

# ============ Page Config ============
st.set_page_config(
    page_title="🎬 Step 1: Script Upload & Cleaning",
    page_icon="📄",
    layout="wide",
)

# ============ Hide Default Sidebar Nav ============
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
    <h1 style='color:#e63946;'>📄 Step 1: Script Upload & Cleaning</h1>
    <p style='color:#adb5bd; font-size:16px;'>
        Upload a movie script in PDF format. BollyAI will:
        <ul>
            <li>🧠 Extract character dialogues using `PyMuPDF`</li>
            <li>👤 Identify speakers using `spaCy`</li>
            <li>🚻 Predict gender using `gender-guesser`</li>
        </ul>
    </p>
    <hr style='border:1px solid #444;'/>
""", unsafe_allow_html=True)

# ============ File Upload ============
uploaded_file = st.file_uploader("📤 Upload Movie Script (PDF)", type="pdf")

if uploaded_file:
    with st.spinner("🔍 Analyzing script and detecting genders..."):
        df = process_pdf(uploaded_file)

    if df is not None and not df.empty:
        st.success(f"✅ Extracted {len(df)} gender-tagged dialogues!")
        st.dataframe(df.head(10), use_container_width=True)

        # 📝 Generate dynamic filename
        clean_name = uploaded_file.name.rsplit(".", 1)[0]
        output_filename = f"cleaned_{clean_name}.csv"

        # 📥 Download cleaned CSV
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_bytes,
            file_name=output_filename,
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No valid gender-tagged lines found. Try a different script.")
