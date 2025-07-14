# pages/page_1_Data_Cleaning.py

import streamlit as st
import pandas as pd
from modules.data_cleaning import process_pdf

st.set_page_config(page_title="🎬 Step 1: Script Upload & Cleaning", layout="wide")
st.title("🎬 Step 1: Script Upload & Cleaning")
st.markdown("""
Upload a movie script PDF. The app will extract dialogues, identify characters using spaCy, and assign gender labels using gender-guesser.
""")

uploaded_file = st.file_uploader("📤 Upload Script PDF", type="pdf")

if uploaded_file is not None:
    with st.spinner("🔍 Processing script..."):
        df = process_pdf(uploaded_file)

    if df is not None and not df.empty:
        st.success(f"✅ Extracted {len(df)} gendered lines.")
        st.dataframe(df.head(10), use_container_width=True)

        # 📝 Generate dynamic CSV filename based on PDF
        original_name = uploaded_file.name.rsplit(".", 1)[0]
        output_filename = f"cleaned_{original_name}.csv"

        # 🔄 In-memory CSV download
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_bytes,
            file_name=output_filename,
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No valid gendered lines found in this script.")
