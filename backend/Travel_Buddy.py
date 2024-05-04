import datetime
import seaborn as sns

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Travel Buddy Matching", page_icon="🌍")

st.sidebar.header("Travel Buddy Matching")
st.markdown("# Travel Buddy Matching")
st.write(
    """Here you can find travel buddies that match your vibe!"""
)

# User inputs
date_input = st.date_input(
    "Select day",
    value=[datetime.date(2024, 5, 5), datetime.date(2024, 5, 5)],
    min_value=datetime.date.today(),
)



df_user = pd._read_csv('')

if st.button("Search Travel Vibe Matching Buddies"):
    matches_data = pd.read_csv('')
    df_potential_matches = pd.DataFrame(matches_data)
    df_potential_matches["compatibility_score"] = (
        (df_potential_matches["danceability"] - df_user["danceability"].values[0]) ** 2
        + (df_potential_matches["energy"] - df_user["energy"].values[0]) ** 2
        + (df_potential_matches["key"] - df_user["key"].values[0]) ** 2
        + (df_potential_matches["loudness"] - df_user["loudness"].values[0]) ** 2
        + (df_potential_matches["instrumentalness"] - df_user["instrumentalness"].values[0]) ** 2
        + (df_potential_matches["liveness"] - df_user["liveness"].values[0]) ** 2
        + (df_potential_matches["valence"] - df_user["valence"].values[0]) ** 2
        + (df_potential_matches["tempo"] - df_user["tempo"].values[0]) ** 2
        + (df_potential_matches["duration_ms"] - df_user["duration_ms"].values[0]) ** 2
        + (df_potential_matches["time_signature"] - df_user["time_signature"].values[0])
        ** 2
    ) ** 0.5

    df_potential_matches = df_potential_matches.sort_values(by='compatibility_score')
    top_matches = df_potential_matches.head(3)
    data_to_insert = top_matches.to_dict(orient='records')

