# pages/page_7_Trailer_Visualization.py

import streamlit as st
import os
from modules.trailer_viz import generate_trailer_plots
from PIL import Image
from modules.sidebar import render_sidebar

st.set_page_config(page_title="🎞️ Step 7: Trailer Emotion Trends", layout="wide")
render_sidebar()
st.title("🎞️ Step 7: Gender–Emotion Analysis in Trailers")

uploaded_file = st.file_uploader("🎥 Upload trailer emotion CSV", type=["csv"])

if uploaded_file:
    st.success("✅ CSV uploaded. Generating plots...")
    file_path = os.path.join("data", "uploaded_trailer_data.csv")
    os.makedirs("data", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    generate_trailer_plots(file_path, output_dir="output")

    st.markdown("### 📊 Emotion Distribution by Gender")
    st.image("output/plot1_emotion_count_by_gender.png")

    st.markdown("### 📊 Gender-wise Emotion Percentages")
    st.image("output/plot2_emotion_percentage_by_gender.png")

    st.markdown("### 📈 Emotion Trends Over Time")
    st.image("output/plot3_emotion_trends_over_time.png")