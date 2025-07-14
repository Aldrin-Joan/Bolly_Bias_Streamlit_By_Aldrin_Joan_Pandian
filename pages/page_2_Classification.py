# pages/page_2_Classification.py

import streamlit as st
import pandas as pd
from io import BytesIO
from modules.classification import classify_stereotype
from config import load_model_tokenizer

st.set_page_config(page_title="🎭 Step 2: Bias Classification", layout="wide")
st.title("🎭 Step 2: Bias Classification using LLM")

uploaded_file = st.file_uploader("📄 Upload cleaned script CSV", type=["csv"])

if uploaded_file:
    # Get filename (without extension) and prepare output filename
    original_name = uploaded_file.name.rsplit(".", 1)[0]
    output_filename = f"{original_name}_classified.csv"

    # Load input data
    df = pd.read_csv(uploaded_file)
    st.write("✅ Uploaded Data Preview", df.head())

    # Load model/tokenizer
    with st.spinner("🚀 Loading model..."):
        tokenizer, model = load_model_tokenizer()

    # Run classification
    with st.spinner("🧠 Classifying gender stereotypes..."):
        from tqdm import tqdm
        tqdm.pandas()
        df["stereotype_type"] = df["line"].progress_apply(lambda line: classify_stereotype(line, tokenizer, model))

    # Show output
    st.success("✅ Classification complete!")
    st.dataframe(df.head(10), use_container_width=True)

    # Convert to CSV in memory
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Annotated CSV", data=csv_bytes, file_name=output_filename, mime="text/csv")
