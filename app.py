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

df = pd.read_csv("data/songs_with_audio_feature.csv")
st.subheader("Dataset Preview")

st.dataframe(df.head())

st.dataframe(df.head())
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
    )
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

st.plotly_chart(fig, use_container_width=True)

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
    use_container_width=True
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
    use_container_width=True
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

st.plotly_chart(fig, use_container_width=True)

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

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("📊 Popularity Distribution")

fig = px.histogram(
    filtered_df,
    x="popularity",
    nbins=30,
    title="Distribution of Song Popularity"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

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

st.plotly_chart(fig, use_container_width=True)
