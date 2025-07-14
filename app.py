# app.py

import streamlit as st

st.set_page_config(
    page_title="Bollywood Bias Buster",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎬 Bollywood Bias Buster")
st.markdown(
    """
    Welcome to **Bolly AI 2.0** – a gender bias detection and remediation toolkit for Bollywood media!

    Use the sidebar to navigate through the different modules:
    - 📄 Upload & clean script data
    - 🧠 Classify gender stereotypes
    - 📊 Visualize gender bias
    - ✍️ Rewrite biased dialogues
    - 📁 Generate final reports
    - 🖼️ Analyze poster bias
    - 🎞️ Trailer emotion trends
    - 📚 Wikipedia gender analytics
    """
)