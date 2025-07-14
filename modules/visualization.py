# modules/visualization.py

import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO, BytesIO

def generate_bias_visualizations(csv_path):
    df = pd.read_csv(csv_path)

    if 'gender' not in df.columns or 'stereotype_type' not in df.columns:
        raise ValueError("CSV must contain 'gender' and 'stereotype_type' columns.")

    # Step 1: Overall stereotype distribution
    overall_bias_counts = df['stereotype_type'].value_counts()
    overall_bias_percentages = (overall_bias_counts / overall_bias_counts.sum()) * 100
    overall_csv_io = StringIO()
    overall_bias_percentages.to_csv(overall_csv_io, index_label="stereotype_type", header=["percentage"])
    overall_csv_io.seek(0)

    # Step 2: Gender-wise stereotype breakdown
    bias_by_gender = df.groupby(['gender', 'stereotype_type']).size().unstack(fill_value=0)
    bias_by_gender_percent = bias_by_gender.div(bias_by_gender.sum(axis=1), axis=0) * 100
    gender_csv_io = StringIO()
    bias_by_gender_percent.to_csv(gender_csv_io, index_label="gender")
    gender_csv_io.seek(0)

    # Step 3: Visualization as in-memory PNG
    fig, ax = plt.subplots(figsize=(10, 6))
    overall_bias_percentages.sort_values(ascending=True).plot(kind='barh', color='skyblue', ax=ax)
    ax.set_xlabel("Percentage")
    ax.set_title("Overall Stereotype Distribution")
    plt.tight_layout()

    img_buffer = BytesIO()
    fig.savefig(img_buffer, format="png")
    plt.close(fig)
    img_buffer.seek(0)

    return overall_csv_io, gender_csv_io, img_buffer
