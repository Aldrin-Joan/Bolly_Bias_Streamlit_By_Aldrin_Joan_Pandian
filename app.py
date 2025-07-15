import streamlit as st

# ============ Page Config ============
st.set_page_config(
    page_title="BollyAI 2.0 – Bollywood Bias Buster",
    page_icon="🎬",
    layout="wide",
)

# ============ Hide default sidebar nav ============
hide_nav_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="stSidebar"] {
            background-color: #111827;
            padding: 1rem;
            width: 220px;
        }
    </style>
"""
st.markdown(hide_nav_style, unsafe_allow_html=True)

# ============ Custom Sidebar ============
with st.sidebar:
    st.markdown("<h2 style='color:#f72585;'>📁 BollyAI 2.0</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    if st.button("📄 1. Data Cleaning"):
        st.switch_page("pages/page_1_data_cleaning.py")

    if st.button("🧠 2. Classification"):
        st.switch_page("pages/page_2_Classification.py")

    if st.button("📊 3. Visualization"):
        st.switch_page("pages/page_3_Visualization.py")

    if st.button("✍️ 4. Rewriting"):
        st.switch_page("pages/page_4_Rewrite.py")

    if st.button("📁 5. Reports"):
        st.switch_page("pages/page_5_Reports.py")

    if st.button("🖼️ 6. Poster Bias"):
        st.switch_page("pages/page_6_Poster_Analysis.py")

    if st.button("🎞️ 7. Trailer Trends"):
        st.switch_page("pages/page_7_Trailer_Visualization.py")

    if st.button("📚 8. Wiki Analysis"):
        st.switch_page("pages/page_8_Wiki_Analysis.py")

    st.markdown("---")
    st.markdown(
        "<p style='font-size:13px; color:#aaa;'>Made with ❤️ by Aldrin</p>",
        unsafe_allow_html=True
    )

# ============ Main Header ============
st.markdown("""
    <h1 style='color:#e63946; font-size: 40px;'>🎬 BollyAI 2.0 – Bollywood Bias Buster</h1>
    <h4 style='color:#adb5bd;'>Detect, Analyze, and Fix Gender Bias in Bollywood Media using LLMs & Vision Models</h4>
    <hr style='border:1px solid #444;'/>
""", unsafe_allow_html=True)

# ============ Project Overview ============
st.markdown("""
<div style="background-color:#1e1e1e; padding:1.5rem; border-radius:10px; border:1px solid #333;">
    <h3 style='color:#ffd60a;'>📂 Project Overview</h3>
    <ul style='color:#d3d3d3; font-size:16px;'>
        <li>📄 <strong>Script Data Cleaning</strong> – Upload raw movie scripts and extract dialogue lines tagged with character names and gender.</li>
        <li>🧠 <strong>Bias Classification</strong> – Use a local Mistral model to classify lines based on 14 gender stereotype categories.</li>
        <li>📊 <strong>Bias Visualization</strong> – Generate bar charts, pie plots, and severity scores to visualize bias by category and gender.</li>
        <li>✍️ <strong>Stereotype Rewriting</strong> – Rewrite biased lines into neutral, inclusive alternatives using LLM-based suggestions.</li>
        <li>📁 <strong>Report Generation</strong> – Export all bias insights and rewrites into a downloadable CSV + PDF feedback report.</li>
        <li>🖼️ <strong>Poster Bias Detection</strong> – Use LLaVA to analyze posters for visual gender imbalance and suggest content tweaks.</li>
        <li>🎞️ <strong>Trailer Emotion Trends</strong> – Analyze emotion–gender dynamics in video trailers using emotion-labeled frame data.</li>
        <li>📚 <strong>Wikipedia Bias Analytics</strong> – Explore gender bias in public knowledge using adjectives, verbs, centrality, and song stats.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
