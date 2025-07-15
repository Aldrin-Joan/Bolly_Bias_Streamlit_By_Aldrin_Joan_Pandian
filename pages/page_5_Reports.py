# pages/page_5_Reports.py

import streamlit as st
import pandas as pd
import uuid
import tempfile
from modules.report_generation import generate_feedback_report
from modules.sidebar import render_sidebar

st.set_page_config(page_title="📊 Step 5: Feedback Report", layout="wide")
render_sidebar()  # 👈 And call this
st.title("📊 Step 5: Generate Feedback Report (CSV + PDF)")
st.markdown("Upload the rewritten script CSV and generate a ranked feedback report.")

uploaded_file = st.file_uploader("📄 Upload Phase 4A Rewrite CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("✅ Uploaded Data Preview", df.head())

    original_name = uploaded_file.name.rsplit(".", 1)[0]
    base_id = original_name + "_" + uuid.uuid4().hex[:6]

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name, index=False)
        csv_out, pdf_out = generate_feedback_report(tmp.name)

    with open(csv_out, "rb") as f1:
        st.download_button(
            "📥 Download Feedback Report (CSV)",
            f1,
            file_name=f"{base_id}_feedback_report.csv"
        )

    with open(pdf_out, "rb") as f2:
        st.download_button(
            "📄 Download Feedback Report (PDF)",
            f2,
            file_name=f"{base_id}_feedback_report.pdf"
        )