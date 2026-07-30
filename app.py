import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Spotify Songs Dashboard",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Spotify Songs Analytics Dashboard")

st.write("Interactive dashboard for analyzing Spotify songs.")
df = pd.read_csv("data/songs_with_audio_feature.csv")

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.markdown("---")

st.subheader("🔎 10 Key Questions")
st.markdown(
    """
    1. Which artists have the highest average popularity?
    2. How has average song popularity changed by release year?
    3. Are more danceable songs generally more popular?
    4. Which songs are the top 10 most popular?
    5. How does explicit vs non-explicit status affect average popularity?
    6. Which years have the highest average popularity?
    7. Do higher-energy songs score better in popularity?
    8. How do acousticness and energy compare in relation to popularity?
    9. Which audio features are most strongly correlated with popularity?
    10. How do tempo and valence relate to popularity?
    """
)

st.markdown("---")

st.subheader("📌 Answering the Questions")

# Year filter
year_range = st.sidebar.slider(
    "Select Release Year",
    int(df["year"].min()),
    int(df["year"].max()),
    (
        int(df["year"].min()),
        int(df["year"].max())
    ),
    key="year_range_questions"
)

filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]

question_corr = filtered_df[
    ["danceability", "energy", "acousticness", "valence", "tempo", "popularity"]
].corr()["popularity"].round(3)

st.markdown("### Q1. Artists with the highest average popularity")

artist_list = (
    filtered_df.groupby("artist_names")
    .agg(Average_Popularity=("popularity", "mean"), Songs=("track_name", "count"))
    .reset_index()
)
artist_list = artist_list[artist_list["Songs"] >= 5].sort_values("Average_Popularity", ascending=False).head(10)
fig = px.bar(
    artist_list,
    x="Average_Popularity",
    y="artist_names",
    orientation="h",
    title="Top Artists by Average Popularity",
)
fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True, key="chart_top_artists")

st.markdown("### Q2. Popularity change by release year")
year_popularity = (
    filtered_df.groupby("year")["popularity"]
    .mean()
    .reset_index()
)
fig = px.line(
    year_popularity,
    x="year",
    y="popularity",
    markers=True,
    title="Average Popularity by Release Year"
)
fig.update_layout(template="plotly_white", title_x=0.5)
st.plotly_chart(fig, use_container_width=True, key="chart_popularity_time")

st.markdown("### Q3. Danceability vs popularity")
st.write(f"Correlation between danceability and popularity: {question_corr['danceability']}")
fig = px.scatter(
    filtered_df,
    x="danceability",
    y="popularity",
    color="energy",
    hover_data=["track_name", "artist_names"],
    title="Danceability vs Popularity"
)
fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True, key="chart_danceability_popularity")

st.markdown("### Q4. Top 10 most popular songs")
top_songs = filtered_df.sort_values("popularity", ascending=False).head(10)
fig = px.bar(
    top_songs,
    x="popularity",
    y="track_name",
    orientation="h",
    color="popularity",
    title="Top 10 Most Popular Songs",
    color_continuous_scale="Viridis"
)
fig.update_layout(template="plotly_white", yaxis=dict(categoryorder="total ascending"))
st.plotly_chart(fig, use_container_width=True, key="chart_top_songs")

st.markdown("### Q5. Explicit vs non-explicit popularity")
explicit_summary = (
    filtered_df.groupby("explicit")["popularity"]
    .mean()
    .reset_index(name="Average Popularity")
)
st.table(explicit_summary)

st.markdown("### Q6. Years with the highest average popularity")
top_years = (
    filtered_df.groupby("year")["popularity"]
    .mean()
    .reset_index()
    .sort_values("popularity", ascending=False)
    .head(10)
)
st.table(top_years)

st.markdown("### Q7. Energy vs popularity")
st.write(f"Correlation between energy and popularity: {question_corr['energy']}")

st.markdown("### Q8. Acousticness vs energy relation to popularity")
st.write(
    f"Correlation with popularity — acousticness: {question_corr['acousticness']}, energy: {question_corr['energy']}"
)

st.markdown("### Q9. Audio feature correlations with popularity")
feature_corr = question_corr.drop("popularity").sort_values(ascending=False).reset_index()
feature_corr.columns = ["Feature", "Correlation with Popularity"]
st.table(feature_corr)

st.markdown("### Q10. Tempo, valence, and popularity")
fig = px.scatter(
    filtered_df,
    x="tempo",
    y="valence",
    size="popularity",
    color="popularity",
    hover_data=["track_name", "artist_names"],
    title="Tempo vs Valence (size = popularity)"
)
fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True, key="chart_tempo_valence")

st.markdown("---")

st.subheader("📊 Dashboard Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎵 Total Songs", len(df))

col2.metric("🎤 Total Artists", df["artist_names"].nunique())

col3.metric("⭐ Average Popularity", round(df["popularity"].mean(), 1))

col4.metric("💃 Average Danceability", round(df["danceability"].mean(), 2))

st.sidebar.header("🎛️ Filters")

# Year filter
year_range = st.sidebar.slider(
    "Select Release Year",
    int(df["year"].min()),
    int(df["year"].max()),
    (
        int(df["year"].min()),
        int(df["year"].max())
    ),
    key="year_range_dashboard"
)

filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]

st.markdown("---")

st.subheader("📈 Average Song Popularity Over Time")

year_popularity = (
    filtered_df.groupby("year")["popularity"]
    .mean()
    .reset_index()
)

fig = px.line(
    year_popularity,
    x="year",
    y="popularity",
    markers=True,
    title="Average Popularity by Release Year"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True, key="chart_average_popularity_over_time")

artist_list = sorted(df["artist_names"].unique())

selected_artist = st.sidebar.selectbox(
    "Select Artist",
    ["All Artists"] + artist_list
)

if selected_artist != "All Artists":
    filtered_df = filtered_df[
        filtered_df["artist_names"] == selected_artist
    ]
st.markdown("---")

st.subheader("💃 Danceability vs Popularity")

fig = px.scatter(
    filtered_df,
    x="danceability",
    y="popularity",
    color="energy",
    hover_data=[
        "track_name",
        "artist_names"
    ],
    title="Do More Danceable Songs Become More Popular?"
)

fig.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="chart_popularity_over_time"
)
st.markdown("---")

st.subheader("🎤 Top 10 Artists by Popularity")

top_artists = (
    filtered_df.groupby("artist_names")
    .agg(
        Average_Popularity=("popularity","mean"),
        Songs=("track_name","count")
    )
    .reset_index()
)


top_artists = top_artists[
    top_artists["Songs"] >= 5
]


top_artists = (
    top_artists
    .sort_values(
        "Average_Popularity",
        ascending=False
    )
    .head(10)
)


fig = px.bar(
    top_artists,
    x="Average_Popularity",
    y="artist_names",
    orientation="h",
    title="Top Artists With Highest Average Popularity"
)


fig.update_layout(
    template="plotly_white"
)


st.plotly_chart(
    fig,
    use_container_width=True,
    key="chart_danceability_vs_popularity"
)
st.markdown("---")

st.subheader("🎵 Top 10 Most Popular Songs")

top_songs = (
    filtered_df.sort_values("popularity", ascending=False)
    .head(10)
)

fig = px.bar(
    top_songs,
    x="popularity",
    y="track_name",
    orientation="h",
    color="popularity",
    title="Top 10 Most Popular Songs",
    color_continuous_scale="Viridis"
)

fig.update_layout(
    template="plotly_white",
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig, use_container_width=True, key="chart_top_10_songs")

st.markdown("---")

st.subheader("🎧 Explicit vs Non-Explicit Songs")

explicit_count = (
    filtered_df["explicit"]
    .value_counts()
    .reset_index()
)

explicit_count.columns = ["Explicit", "Count"]

fig = px.pie(
    explicit_count,
    names="Explicit",
    values="Count",
    hole=0.4,
    title="Explicit Song Distribution"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True, key="chart_explicit_distribution")

st.markdown("---")

st.subheader("📊 Popularity Distribution")

fig = px.histogram(
    filtered_df,
    x="popularity",
    nbins=30,
    title="Distribution of Song Popularity"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True, key="chart_popularity_distribution")

import plotly.figure_factory as ff
st.markdown("---")

st.subheader("🔥 Correlation Heatmap")

corr = filtered_df[
    [
        "danceability",
        "energy",
        "valence",
        "acousticness",
        "speechiness",
        "liveness",
        "tempo",
        "popularity"
    ]
].corr()

fig = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    annotation_text=corr.round(2).values,
    colorscale="Viridis"
)

fig.update_layout(
    template="plotly_white",
    title="Correlation Between Audio Features"
)

st.plotly_chart(fig, use_container_width=True, key="chart_correlation_heatmap")
