import asyncio
import json

import numpy as np
import pandas as pd
import streamlit as st

import neurofeedback
from spotify import Spotify

st.set_page_config(page_title="Mood Switch", page_icon="📈")

st.sidebar.header("Mood Switch")
st.markdown("# Mood Switch")
st.write("""Here you can set the vibe of your travel plans""")

st.divider()
st.write("What type of Vibe would you like your trip to be?")
option_a = st.checkbox("Calm and Relaxing")
option_b = st.checkbox("High Energy & Adventurous")
option_t = st.checkbox("Self Exploration and Intellectual")

placeholder = st.empty()
st.divider()

col1, col2 = st.columns(2)
df_eeg = pd.DataFrame(columns=["alpha_metric", "beta_metric", "theta_metric"])



def get_df(feedback_type, merged_df):
    if feedback_type == "calm and relaxing":
        merged_df["danceability_var"] = (0.4 - merged_df["danceability"]) ** 2
        merged_df["energy_var"] = (0.4 - merged_df["energy"]) ** 2
        merged_df["speechiness_var"] = (0.7 - merged_df["speechiness"]) ** 2
        merged_df["acousticness_var"] = (0.7 - merged_df["acousticness"]) ** 2
        merged_df["instrumentalness_var"] = (0.5 - merged_df["instrumentalness"]) ** 2
        merged_df["liveness_var"] = (0.8 - merged_df["liveness"]) ** 2
        merged_df["valence_var"] = (0.8 - merged_df["valence"]) ** 2
    elif feedback_type == "octane and adventurous":
        merged_df["danceability_var"] = (0.7 - merged_df["danceability"]) ** 2
        merged_df["energy_var"] = (0.7 - merged_df["energy"]) ** 2
        merged_df["speechiness_var"] = (0.4 - merged_df["speechiness"]) ** 2
        merged_df["acousticness_var"] = (0.4 - merged_df["acousticness"]) ** 2
        merged_df["instrumentalness_var"] = (0.4 - merged_df["instrumentalness"]) ** 2
        merged_df["liveness_var"] = (0.5 - merged_df["liveness"]) ** 2
        merged_df["valence_var"] = (0.8 - merged_df["valence"]) ** 2
    elif feedback_type == "focussed":
        merged_df["danceability_var"] = (0.5 - merged_df["danceability"]) ** 2
        merged_df["energy_var"] = (0.5 - merged_df["energy"]) ** 2
        merged_df["speechiness_var"] = (0.6 - merged_df["speechiness"]) ** 2
        merged_df["acousticness_var"] = (0.7 - merged_df["acousticness"]) ** 2
        merged_df["instrumentalness_var"] = (0.7 - merged_df["instrumentalness"]) ** 2
        merged_df["liveness_var"] = (0.5 - merged_df["liveness"]) ** 2
        merged_df["valence_var"] = (0.9 - merged_df["valence"]) ** 2
    elif feedback_type == "high octane and relaxing":
        merged_df["danceability_var"] = (0.7 - merged_df["danceability"]) ** 2
        merged_df["energy_var"] = (0.7 - merged_df["energy"]) ** 2
        merged_df["speechiness_var"] = (0.7 - merged_df["speechiness"]) ** 2
        merged_df["acousticness_var"] = (0.7 - merged_df["acousticness"]) ** 2
        merged_df["instrumentalness_var"] = (0.7 - merged_df["instrumentalness"]) ** 2
        merged_df["liveness_var"] = (0.7 - merged_df["liveness"]) ** 2
        merged_df["valence_var"] = (0.8 - merged_df["valence"]) ** 2
    else:
        raise Exception("unmatched feedback type")

    merged_df = merged_df.sort_values(
        [
            "danceability_var",
            "energy_var",
            "speechiness_var",
            "acousticness_var",
            "instrumentalness_var",
            "liveness_var",
            "valence_var",
        ],
        ascending=[True, True, True, True, True, True, True],
    )

    return merged_df


def create_new_queue(tracks):
    song_names, song_artists, ids = [], [], []
    for item in tracks:
        if item.get("track"):
            item = item["track"]
        ids.append(item["id"])
        song_names.append(item["name"])
        song_artists.append([artist["name"] for artist in item["artists"]])

    audio_features = spotify.get_audio_features(",".join(ids)).json()

    # Import user's playlist (Last 100 songs played)
    df_features = pd.DataFrame(audio_features["audio_features"])
    df_artists = pd.DataFrame({"artists": song_artists})
    df_song_names = pd.DataFrame({"tracks": song_names})
    df_final = pd.concat([df_artists, df_song_names, df_features], axis=1)

    return df_final


if col1.button("Start Playing Vibey Music"):
    spotify = Spotify()
    recent_tracks = spotify.get_saved_tracks()
    df_final = create_new_queue(recent_tracks.json()["items"])

    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 3)
    chart = st.line_chart(last_rows)

    if option_a is True and option_t is False and option_b is False:
        st.write("Creating Calm and Relaxing Vibes")
        df_after = get_df("calm and relaxing", df_final)
        spotify.play_track({"uris": [f"spotify:track:{df_after.iloc[0, 14]}"]})
        st.write("Playing ...")
        st.table(df_after[["tracks", "artists"]].head(2))

        # QUEUE
        while True:
            alpha_metric, beta_metric, theta_metric = next(neurofeedback.neurofeedback_fn())
            new_rows = np.array([[alpha_metric, beta_metric, theta_metric]])
            chart.add_rows(new_rows)
            df_eeg = pd.concat([df_eeg, pd.DataFrame([{
                "alpha_metric": alpha_metric,
                "beta_metric": beta_metric,
                "theta_metric": theta_metric
            }])], ignore_index=True)

            if len(df_eeg) % 10 == 0:
                if np.percentile(df_eeg["alpha_metric"], 75) - np.percentile(df_eeg["alpha_metric"], 25) > 0:
                    recommendations = spotify.get_recommendations(
                        {"seed_tracks": df_after.iloc[0, 14]}
                    )
                    df_after = create_new_queue(recommendations.json()["tracks"])
                    df_after = df_after.iloc[1:]
                    st.table(df_after[["tracks", "artists"]].head(2))

                    spotify.add_to_queue({"uri": recommendations.json()['tracks'][1]['uri']})
                    print("Use metrics from the current spotify song to recommend the next song which is similar to the current song")
                    print("You are more relaxed")
                elif np.percentile(df_eeg["alpha_metric"], 75) - np.percentile(df_eeg["alpha_metric"], 25) < 0:
                    # Get next song in queue
                    df_after = df_after.iloc[1:]
                    st.table(df_after[["tracks", "artists"]].head(2))
                    print("Try next song from the initially made playlist")
                    print("Checking for neurofeedback with other songs for alpha waves")

    elif option_b is True and option_t is False and option_a is False:
        st.write("Creating High Octane and Adventurous Vibe")
        df_after = get_df("octane and adventurous", df_final)
        spotify.play_track({"uris": [f"spotify:track:{df_after.iloc[0, 14]}"]})
        st.write("Playing ...")
        st.table(df_after[["tracks", "artists"]].head(2))

        while True:
            alpha_metric, beta_metric, theta_metric = next(neurofeedback.neurofeedback_fn())
            new_rows = np.array([[alpha_metric, beta_metric, theta_metric]])
            chart.add_rows(new_rows)
            df_eeg = pd.concat([df_eeg, pd.DataFrame([{
                "alpha_metric": alpha_metric,
                "beta_metric": beta_metric,
                "theta_metric": theta_metric
            }])], ignore_index=True)

            if len(df_eeg) % 10 == 0:
                if np.percentile(df_eeg["beta_metric"], 75) - np.percentile(df_eeg["alpha_metric"], 25) > 0:
                    # Get recommendations
                    recommendations = spotify.get_recommendations(
                        {"seed_tracks": df_final.iloc[0, 14]}
                    )
                    df_after = create_new_queue(recommendations.json()["tracks"])
                    df_after = df_after.iloc[1:]
                    st.table(df_after[["tracks", "artists"]].head(2))
                    spotify.add_to_queue({"uri": recommendations.json()['tracks'][1]['uri']})
                    print("Use metrics from the current spotify song to recommend the next song which is similar to the current song")
                elif np.percentile(df_eeg["beta_metric"], 75) - np.percentile(df_eeg["alpha_metric"], 25) < 0:
                    # Play next song in queue
                    df_after = df_after.iloc[1:]
                    st.table(df_after[["tracks", "artists"]].head(2))
                    print("Try next song from the initially made playlist")

    elif option_t is True and option_a is False and option_b is False:
        st.write("Creating Focussed Vibe")
        df_after = get_df("focussed", df_final)
        spotify.play_track({"uris": [f"spotify:track:{df_after.iloc[0, 14]}"]})
        st.write("Playing ...")
        st.table(df_after[["tracks", "artists"]].head(2))

        while True:
            alpha_metric, beta_metric, theta_metric = next(neurofeedback.neurofeedback_fn())
            new_rows = np.array([[alpha_metric, beta_metric, theta_metric]])
            chart.add_rows(new_rows)
            df_eeg = pd.concat([df_eeg, pd.DataFrame([{
                "alpha_metric": alpha_metric,
                "beta_metric": beta_metric,
                "theta_metric": theta_metric
            }])], ignore_index=True)

            if len(df_eeg) % 10 == 0:
                if np.percentile(df_eeg["theta_metric"], 75) - np.percentile(df_eeg["theta_metric"], 25) > 0:
                    recommendations = spotify.get_recommendations(
                        {"seed_tracks": df_after.iloc[0, 14]}
                    )
                    df_after = create_new_queue(recommendations.json()["tracks"])
                    df_after = df_after.iloc[1:]
                    st.table(df_after[["tracks", "artists"]].head(2))

                    spotify.add_to_queue({"uri": recommendations.json()['tracks'][1]['uri']})
                    print(
                        "Use metrics from the current spotify song to recommend the next song which is similar to the current song"
                    )
                elif np.percentile(df_eeg["theta_metric"], 75) - np.percentile(df_eeg["theta_metric"], 25) < 0:
                    df_after = df_after.iloc[1:]
                    st.table(df_after[["tracks", "artists"]].head(2))
                    print("Try next song from the initially made playlist")

if col2.button("Stop"):
    # This would empty everything inside the container
    placeholder.empty()
