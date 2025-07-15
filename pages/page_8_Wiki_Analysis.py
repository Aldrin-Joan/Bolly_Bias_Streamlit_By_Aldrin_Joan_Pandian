# pages/page_8_Wiki_Analysis.py

import streamlit as st
import os  # ✅ Add this
from modules import wiki_analysis
from modules.sidebar import render_sidebar

st.set_page_config(page_title="📚 Step 8: Wikipedia Gender Bias", layout="wide")
st.title("📚 Step 8: Wikipedia-based Gender Analysis")
render_sidebar()
st.markdown("""
This module performs **Wikipedia-derived** bias analysis across 5 dimensions:
- Verbs over time (by gender)
- Centrality metrics
- Coreference pronoun usage
- Gender in song metadata
- Gender representation ratios
""")

st.divider()

if st.button("📊 Plot Verb Trends Over Time"):
    wiki_analysis.plot_top_verbs_facet(wiki_analysis.male_verb_df, gender="male")
    wiki_analysis.plot_top_verbs_facet(wiki_analysis.female_verb_df, gender="female")

if st.button("📈 Show Centrality Metrics"):
    wiki_analysis.plot_centrality_metrics()

if st.button("🔁 Coreference Analysis"):
    wiki_analysis.plot_coref_distributions()

if st.button("🎵 Song Representation Analysis"):
    wiki_analysis.plot_song_gender_stats()

if st.button("⚖️ Gender Ratio Comparison (Mentions, Cast, Centrality)"):
    output_path = wiki_analysis.generate_gender_ratio_csv()
    if output_path and os.path.exists(output_path):
        with open(output_path, "rb") as f:
            st.download_button("📥 Download Gender Ratio CSV", f, file_name="gender_bias_comparison.csv")
        st.success("✅ Gender ratio report ready for download.")
    else:
        st.error("❌ Failed to generate report.")
