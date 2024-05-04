import datetime

import pandas as pd
import streamlit as st

from database import Database
from spotify import Spotify

database = Database()

st.set_page_config(page_title="Travel Buddy Matching", page_icon="🌍")

st.sidebar.header("Travel Buddy Matching")
st.markdown("# Travel Buddy Matching")
st.write("""Here you can find travel buddies that match your vibe!""")
spotify = Spotify()
recent_tracks = spotify.get_recent_tracks()
ids = []
for item in recent_tracks.json()["items"]:
    ids.append(item["track"]["id"])

# Get audio features
audio_features = spotify.get_audio_features(",".join(ids)).json()
user_data = spotify.get_user_data().json()

# Mean of audio features
df = pd.DataFrame(audio_features["audio_features"])
selected_columns = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "duration_ms",
    "time_signature",
]
means = df[selected_columns].mean()
cols = str(tuple(["spotify_uri"] + selected_columns)).replace("'", "")
row = [user_data["uri"]] + list(means.to_dict().values())

insert_stmt = (
    f"INSERT INTO user_data {cols} VALUES {tuple(row)} "
    f"ON CONFLICT (spotify_uri) DO UPDATE SET "
    f"{', '.join([f'{col}=EXCLUDED.{col}' for col in selected_columns])} RETURNING 1;"
)
database.execute_query(insert_stmt)
spotifyUri = (user_data["uri"],)
displayName = user_data["display_name"]
st.divider()
col1, col2 = st.columns([1, 2])
col1.header(displayName)
col2.markdown(
    """<iframe src="http://localhost:2999/d-solo/edkq6gqgcnjswe/hackupc?orgId=1&from=1714835344593&to=1714856944593&panelId=1" width="450" height="200" frameborder="0"></iframe>""",
    unsafe_allow_html=True,
)
st.divider()

# User inputs
date_input = st.date_input(
    "Select days planned for travel",
    value=[datetime.date(2024, 5, 5), datetime.date(2024, 5, 5)],
    min_value=datetime.date.today(),
)

st.divider()

if st.button("Search Travel Vibe Matching Buddies"):
    # Get database of user's spotify profile
    truncate_stmt = "TRUNCATE current_matches;"
    database.execute_dml_query(truncate_stmt)

    user_stmt = f"SELECT * FROM user_data WHERE spotify_uri = '{spotifyUri[0]}';"
    user_data = database.execute_query(user_stmt)
    df_user = pd.DataFrame(user_data)

    matches_stmt = f"""
          SELECT *,
          CASE
              WHEN departure_date = '{date_input[0]}' AND return_date = '{date_input[1]}' THEN 'BOTH'
              WHEN departure_date = '{date_input[0]}' THEN 'DEPARTURE'
              WHEN return_date = '{date_input[1]}' THEN 'RETURN'
              ELSE 'NONE'
          END AS match_type
          FROM dataset
          WHERE departure_date = '{date_input[0]}'
          OR return_date = '{date_input[1]}';
        """
    matches_data = database.execute_query(matches_stmt)
    df_potential_matches = pd.DataFrame(matches_data)
    df_potential_matches["compatibility_score"] = (
        (df_potential_matches["danceability"] - df_user["danceability"].values[0]) ** 2
        + (df_potential_matches["energy"] - df_user["energy"].values[0]) ** 2
        + (df_potential_matches["danceability"] - df_user["acousticness"].values[0])
        ** 2
        + (df_potential_matches["danceability"] - df_user["speechiness"].values[0]) ** 2
        + (
            df_potential_matches["instrumentalness"]
            - df_user["instrumentalness"].values[0]
        )
        ** 2
        + (df_potential_matches["liveness"] - df_user["liveness"].values[0]) ** 2
        + (df_potential_matches["valence"] - df_user["valence"].values[0]) ** 2
    ) ** 0.5

    df_potential_matches = df_potential_matches.sort_values(by="compatibility_score")
    top_matches = df_potential_matches.head(3)
    data_to_insert = top_matches.to_dict(orient="records")

    insert_query = """
        INSERT INTO current_matches (trip_id, traveller_name, departure_city, arrival_city, return_date, departure_date, trip_length, acousticness, danceability, duration_ms, energy, instrumentalness, liveness, loudness, mode, speechiness, tempo, valence, time_signature, key, match_type, compatibility_score)
        VALUES (:trip_id, :traveller_name, :departure_city, :arrival_city, :return_date,:departure_date,:trip_length, :acousticness, :danceability, :duration_ms, :energy, :instrumentalness , :liveness , :loudness, :mode, :speechiness, :tempo, :valence, :time_signature, :key, :match_type, :compatibility_score);
    """

    database.execute_dml_query(insert_query, params=data_to_insert)

    if len(top_matches) > 0:
        st.subheader(top_matches.iloc[0, 1])
        st.write(top_matches.iloc[0, 20])
        st.markdown(
            """<iframe src="http://localhost:2999/d-solo/edkq6gqgcnjswe/hackupc?orgId=1&from=1714837989251&to=1714859589252&panelId=2" width="450" height="200" frameborder="0"></iframe>""",
            unsafe_allow_html=True,
        )
    if len(top_matches) > 1:
        st.subheader(top_matches.iloc[1, 1])
        st.write(top_matches.iloc[1, 20])
        st.markdown(
            """<iframe src="http://localhost:2999/d-solo/edkq6gqgcnjswe/hackupc?orgId=1&from=1714838067234&to=1714859667234&panelId=3" width="450" height="200" frameborder="0"></iframe>""",
            unsafe_allow_html=True,
        )
    if len(top_matches) > 2:
        st.subheader(top_matches.iloc[2, 1])
        st.write(top_matches.iloc[2, 20])
        st.markdown(
            """<iframe src="http://localhost:2999/d-solo/edkq6gqgcnjswe/hackupc?orgId=1&from=1714838096116&to=1714859696116&panelId=4" width="450" height="200" frameborder="0"></iframe>""",
            unsafe_allow_html=True,
        )
