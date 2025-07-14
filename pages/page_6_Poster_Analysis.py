# pages/page_6_Poster_Analysis.py

import streamlit as st
from PIL import Image
from modules.poster_analysis import detect_poster_bias, generate_poster_pdf

st.set_page_config(page_title="🎨 Step 6: Poster Bias Detection", layout="wide")
st.title("🎨 Step 6: Poster Bias Detection using LLaVA")
st.markdown("Upload a movie poster image to analyze for visual gender bias using **LLaVA-1.5**.")

uploaded_file = st.file_uploader("📤 Upload Poster Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Poster", use_column_width=True)

    with st.spinner("🔍 Analyzing for bias..."):
        result = detect_poster_bias(image)

    st.markdown("### 🎯 Model Output")
    st.code(result)

    with st.spinner("📄 Generating PDF report..."):
        pdf_buffer = generate_poster_pdf(result, image)

    st.download_button(
        label="📥 Download Poster Bias PDF",
        data=pdf_buffer,
        file_name="poster_bias_report.pdf",
        mime="application/pdf"
    )
