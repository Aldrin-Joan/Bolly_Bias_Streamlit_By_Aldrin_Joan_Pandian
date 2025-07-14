# modules/trailer_viz.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["axes.titlesize"] = 14

def generate_trailer_plots(csv_path: str, output_dir: str = "output") -> None:
    os.makedirs(output_dir, exist_ok=True)

    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    # Plot 1: Emotion count by gender
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='emotion', hue='gender', palette='Set2')
    plt.title("Emotion Distribution by Gender in Bollywood Trailers")
    plt.xlabel("Emotion Type")
    plt.ylabel("Number of Frames")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "plot1_emotion_count_by_gender.png"))
    plt.close()

    # Plot 2: Emotion percentage breakdown
    emotion_counts = df.groupby(['gender', 'emotion']).size().reset_index(name='count')
    emotion_counts['percentage'] = emotion_counts.groupby('gender')['count'].transform(lambda x: 100 * x / x.sum())

    plt.figure(figsize=(10, 6))
    sns.barplot(data=emotion_counts, x='emotion', y='percentage', hue='gender', palette='Set2')
    plt.title("Gender-wise Percentage of Expressed Emotions")
    plt.ylabel("Percentage (%)")
    plt.xlabel("Emotion Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "plot2_emotion_percentage_by_gender.png"))
    plt.close()

    # Plot 3: Emotion trends over time
    emotion_over_time = df.groupby(['year', 'gender', 'emotion']).size().reset_index(name='count')

    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=emotion_over_time,
        x='year', y='count',
        hue='emotion', style='gender',
        markers=True, dashes=False, palette='tab10'
    )
    plt.title("Emotion Trends by Gender Over Time")
    plt.xlabel("Year")
    plt.ylabel("Number of Frames")
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.savefig(os.path.join(output_dir, "plot3_emotion_trends_over_time.png"))
    plt.close()