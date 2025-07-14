# pages/page_4_Rewrite.py

import streamlit as st
import pandas as pd
from io import BytesIO
from modules.rewriting import rewrite_biased_line
from config import load_model_tokenizer
from tqdm import tqdm

st.set_page_config(page_title="✍️ Step 4: Rewrite Biased Lines", layout="wide")
st.title("✍️ Step 4: Rewriting Stereotypical Lines")
st.markdown("Upload the bias-annotated CSV (from Step 3). Biased lines will be rewritten using LLM prompts.")

uploaded_file = st.file_uploader("📄 Upload Bias-Annotated CSV", type=["csv"])

if uploaded_file:
    # Dynamically generate download name
    original_name = uploaded_file.name.rsplit(".", 1)[0]
    output_filename = f"{original_name}_rewritten.csv"

    # Load uploaded CSV
    df = pd.read_csv(uploaded_file)
    st.write("✅ Uploaded Data Preview", df.head())

    # Load model and tokenizer
    with st.spinner("🚀 Loading model..."):
        tokenizer, model = load_model_tokenizer()

    # Rewrite biased lines
    with st.spinner("✍️ Rewriting biased lines..."):
        tqdm.pandas()
        df["rewritten_line"] = df.progress_apply(
            lambda row: rewrite_biased_line(row["line"], row["stereotype_type"], tokenizer, model)
            if row["stereotype_type"] != "none" else row["line"],
            axis=1
        )

    # Show output
    st.success("✅ Rewriting complete!")
    st.dataframe(df.head(10), use_container_width=True)

    # Download in-memory
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Rewritten CSV", data=csv_bytes, file_name=output_filename, mime="text/csv")
