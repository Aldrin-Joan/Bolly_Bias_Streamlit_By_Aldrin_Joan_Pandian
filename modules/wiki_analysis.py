import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import re
import streamlit as st
from collections import Counter

sns.set(style="whitegrid")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["axes.titlesize"] = 14

base_path = "data/wikipedia-data"

# ----- VERB ANALYSIS -----
def load_verb_file(filepath):
    years, verbs = [], []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",", 1)
            if len(parts) == 2:
                year = parts[0].strip()
                verb_clean = re.findall(r'\w+', parts[1].strip())
                years.append(int(year))
                verbs.append(verb_clean)
    return pd.DataFrame({"year": years, "verbs": verbs})

male_verb_df = load_verb_file(os.path.join(base_path, "male_verb.csv"))
female_verb_df = load_verb_file(os.path.join(base_path, "female_verb.csv"))

def plot_top_verbs_facet(df, gender="male", top_n=6):
    from matplotlib.ticker import MaxNLocator
    verb_freq_by_year = {}
    for _, row in df.iterrows():
        year = row["year"]
        for verb in row["verbs"]:
            key = (year, verb)
            verb_freq_by_year[key] = verb_freq_by_year.get(key, 0) + 1
    df_verbs = pd.DataFrame([{"year": y, "verb": v, "count": c} for (y, v), c in verb_freq_by_year.items()])
    top_verbs = df_verbs.groupby("verb")["count"].sum().nlargest(top_n).index
    df_top = df_verbs[df_verbs["verb"].isin(top_verbs)]
    g = sns.FacetGrid(df_top, col="verb", col_wrap=3, height=4, sharey=False)
    g.map_dataframe(sns.lineplot, x="year", y="count", marker="o", color="indigo")
    g.set_titles(col_template="{col_name}")
    g.set_axis_labels("Year", "Frequency")
    for ax in g.axes.flatten():
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.tick_params(axis='x', rotation=45)
    plt.suptitle(f"Top {top_n} Verbs Used by {gender.capitalize()} Characters", fontsize=16, y=1.05)
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()
    plt.close()

# ----- CENTRALITY METRICS -----
def plot_centrality_metrics():
    male_centrality = pd.read_csv(os.path.join(base_path, "male_centrality.csv"))
    female_centrality = pd.read_csv(os.path.join(base_path, "female_centrality.csv"))
    male_centrality["gender"] = "male"
    female_centrality["gender"] = "female"
    centrality = pd.concat([male_centrality, female_centrality], ignore_index=True)
    centrality.columns = centrality.columns.str.strip()
    centrality = centrality.loc[:, ~centrality.columns.duplicated()]
    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=centrality,
        x="gender",
        y="Average Centrality",
        hue="gender",
        palette={"male": "#1f77b4", "female": "#ff69b4"},
        errorbar="sd",
        legend=False
    )
    plt.title("Average Centrality by Gender")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()
    plt.close()

# ----- COREFERENCE PRONOUNS -----
def plot_coref_distributions():
    coref = pd.read_csv(os.path.join(base_path, "coref_plot.csv"), usecols=["Movie Name", "Coref Plot"])
    coref.columns = coref.columns.str.strip()
    all_words = " ".join(coref["Coref Plot"].astype(str).str.lower()).split()
    male_pronouns = ["he", "him", "his"]
    female_pronouns = ["she", "her", "hers"]
    pronoun_counts = Counter(word for word in all_words if word in male_pronouns + female_pronouns)
    pronoun_df = pd.DataFrame(pronoun_counts.items(), columns=["pronoun", "count"]).sort_values("count", ascending=False)

    # Bar plot of pronouns
    plt.figure(figsize=(8, 6))
    sns.barplot(data=pronoun_df, x="pronoun", y="count", palette="Set2")
    plt.title("Pronoun Frequency in Coreference Plots")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()
    plt.close()

    # Grouped by gender
    gender_totals_df = pd.DataFrame({
        "gender": ["male", "female"],
        "count": [sum(pronoun_counts[p] for p in male_pronouns), sum(pronoun_counts[p] for p in female_pronouns)]
    })
    plt.figure(figsize=(6, 5))
    sns.barplot(data=gender_totals_df, x="gender", y="count", palette="Set2")
    plt.title("Grouped Gendered Pronoun Totals")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()
    plt.close()

# ----- SONG REPRESENTATION -----
def plot_song_gender_stats():
    songs_db = pd.read_csv(os.path.join(base_path, "songsDB.csv"), on_bad_lines="skip", encoding="utf-8")
    songs_freq = pd.read_csv(os.path.join(base_path, "songsFrequency.csv"), on_bad_lines="skip", encoding="utf-8")

    songs_db.columns = songs_db.columns.str.strip().str.lower()
    songs_freq.columns = songs_freq.columns.str.strip().str.upper()

    if "movietitle_year" in songs_db.columns:
        songs_db["year"] = songs_db["movietitle_year"].str.extract(r"_(\d{4})")[0]
    else:
        st.error("❌ Column 'movietitle_year' not found in songsDB.csv.")
        return

    songs_db = songs_db.dropna(subset=["year"])
    songs_db["year"] = songs_db["year"].astype(int)

    # Plot 1: Total songs per year by gender
    song_counts = songs_db.groupby(["year", "gender"])["song_count"].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=song_counts, x="year", y="song_count", hue="gender", marker="o", palette="Set2")
    plt.title("Total Songs per Year by Gender")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()
    plt.close()

    # Plot 2: Unique singers per year by gender
    unique_singers = songs_db.groupby(["year", "gender"])["singer_name"].nunique().reset_index(name="unique_singers")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=unique_singers, x="year", y="unique_singers", hue="gender", marker="o", palette="Set1")
    plt.title("Unique Singers per Year by Gender")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()
    plt.close()

    # Plot 3: Average songs per singer per year
    songs_per_singer = songs_db.groupby(["year", "gender"]).agg(
        total_songs=("song_count", "sum"),
        total_singers=("singer_name", "nunique")
    ).reset_index()
    songs_per_singer["avg_songs_per_singer"] = songs_per_singer["total_songs"] / songs_per_singer["total_singers"]
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=songs_per_singer, x="year", y="avg_songs_per_singer", hue="gender", marker="o", palette="Set2")
    plt.title("Average Songs per Singer by Gender")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()
    plt.close()

# ----- GENDER RATIOS CSV -----
def generate_gender_ratio_csv():
    male_df = pd.read_csv(os.path.join(base_path, "male_mentions_centrality.csv"))
    female_df = pd.read_csv(os.path.join(base_path, "female_mentions_centrality.csv"))
    male_df.columns = female_df.columns = [c.strip().lower().replace(" ", "_") for c in male_df.columns]

    male_grouped = male_df.groupby("movie_name").agg({
        "mentions": "sum",
        "total_centrality": "sum",
        "average_centrality": "mean",
        "cast": "count"
    }).rename(columns={
        "mentions": "male_mentions",
        "total_centrality": "male_total_centrality",
        "average_centrality": "male_avg_centrality",
        "cast": "male_cast_count"
    })

    female_grouped = female_df.groupby("movie_name").agg({
        "mentions": "sum",
        "total_centrality": "sum",
        "average_centrality": "mean",
        "cast": "count"
    }).rename(columns={
        "mentions": "female_mentions",
        "total_centrality": "female_total_centrality",
        "average_centrality": "female_avg_centrality",
        "cast": "female_cast_count"
    })

    combined_df = pd.merge(male_grouped, female_grouped, on="movie_name", how="inner")
    epsilon = 1e-6
    combined_df["mentions_ratio"] = combined_df["male_mentions"] / (combined_df["female_mentions"] + epsilon)
    combined_df["centrality_ratio"] = combined_df["male_total_centrality"] / (combined_df["female_total_centrality"] + epsilon)
    combined_df["cast_ratio"] = combined_df["male_cast_count"] / (combined_df["female_cast_count"] + epsilon)
    combined_df["avg_centrality_diff"] = combined_df["male_avg_centrality"] - combined_df["female_avg_centrality"]

    output_path = os.path.join("output", "gender_bias_comparison.csv")
    os.makedirs("output", exist_ok=True)
    combined_df.to_csv(output_path, index=True)

    return output_path  # ✅ Used by Streamlit download button
