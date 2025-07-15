# modules/visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_bias_visualizations(csv_path, output_dir="data"):
    df = pd.read_csv(csv_path)

    if 'gender' not in df.columns or 'stereotype_type' not in df.columns:
        raise ValueError("CSV must contain 'gender' and 'stereotype_type' columns.")

    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Overall stereotype distribution
    overall_bias_counts = df['stereotype_type'].value_counts()
    overall_bias_percentages = (overall_bias_counts / overall_bias_counts.sum()) * 100
    overall_csv_path = os.path.join(output_dir, "bias_scores_overall.csv")
    overall_bias_percentages.to_csv(overall_csv_path, index_label="stereotype_type", header=["percentage"])

    # Step 2: Gender-wise stereotype breakdown
    bias_by_gender = df.groupby(['gender', 'stereotype_type']).size().unstack(fill_value=0)
    bias_by_gender_percent = bias_by_gender.div(bias_by_gender.sum(axis=1), axis=0) * 100
    gender_csv_path = os.path.join(output_dir, "bias_scores_by_gender.csv")
    bias_by_gender_percent.to_csv(gender_csv_path, index_label="gender")

    # Step 3: Visualization as PNG
    fig, ax = plt.subplots(figsize=(10, 6))
    overall_bias_percentages.sort_values(ascending=True).plot(kind='barh', color='skyblue', ax=ax)
    ax.set_xlabel("Percentage")
    ax.set_title("Overall Stereotype Distribution")
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "bias_trends_overall.png")
    fig.savefig(plot_path)
    plt.close(fig)

    return overall_csv_path, gender_csv_path, plot_path
