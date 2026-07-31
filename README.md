# Spotify Songs Analytics Dashboard

Interactive Streamlit dashboard for exploring Spotify song popularity and audio features.

## Overview

This repository contains a Streamlit app that analyzes a Spotify song dataset and presents interactive visualizations for:

- artist popularity
- release year trends
- danceability vs popularity
- explicit vs non-explicit popularity
- audio feature correlations
- top songs by popularity
- tempo and valence relationships

The dashboard loads data from `data/songs_with_audio_feature.csv` and uses `plotly` for interactive charts.

## Files

- `app.py` — main Streamlit application
- `requirements.txt` — Python dependencies
- `data/songs_with_audio_feature.csv` — primary dataset used by the dashboard
- `data/spotify_songs.csv` — additional dataset file included in the workspace
- `notebook.ipynb` — exploratory notebook (optional)
- `images/` — image assets
- `pptx/` — presentation files

## Dataset

The dataset includes 35,200 songs and the following audio feature fields:

- `track_id`
- `track_name`
- `album_id`
- `artist_ids`
- `artist_names`
- `valence`
- `year`
- `acousticness`
- `danceability`
- `duration_ms`
- `energy`
- `explicit`
- `instrumentalness`
- `key`
- `liveness`
- `loudness`
- `mode`
- `popularity`
- `release_date`
- `speechiness`
- `tempo`

## Requirements

This project requires Python and the packages listed in `requirements.txt`, including:

- `streamlit`
- `pandas`
- `plotly`

## Setup

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the dashboard

From the project root directory, run:

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Dashboard features

The app includes the following interactive analyses:

1. Top artists by average popularity
2. Average popularity by release year
3. Danceability vs popularity scatter plot
4. Top 10 most popular songs
5. Explicit vs non-explicit popularity comparison
6. Years with the highest average popularity
7. Energy vs popularity correlation
8. Acousticness and energy correlation with popularity
9. Audio feature correlations with popularity
10. Tempo and valence relationships with popularity

## Notes

- The dashboard uses the `year` and audio feature columns to filter and compute correlations.
- Ensure `data/songs_with_audio_feature.csv` is present before launching the app.
- The app is intended for exploration and visualization of Spotify song trends.
