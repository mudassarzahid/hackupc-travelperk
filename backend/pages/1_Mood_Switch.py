import os

import pandas as pd
import streamlit as st

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

if col1.button("Start Playing Vibey Music"):
    spotify = Spotify()
    recent_tracks = spotify.get_saved_tracks()

    song_names, song_artists, ids = [], [], []
    for item in recent_tracks.json()["items"]:
        ids.append(item["track"]["id"])
        song_names.append(item["track"]["name"])
        song_artists.append([artist["name"] for artist in item["track"]["artists"]])

    audio_features = spotify.get_audio_features(",".join(ids)).json()

    # Import user's playlist (Last 100 songs played)
    df_features = pd.DataFrame(audio_features["audio_features"])
    df_artists = pd.DataFrame({"artists": song_artists})
    df_song_names = pd.DataFrame({"tracks": song_names})
    df_final = pd.concat([df_artists, df_song_names, df_features], axis=1)

    df_final["danceability_var"] = (0.5 - df_final["danceability"]) ** 2
    df_final["energy_var"] = (0.5 - df_final["energy"]) ** 2
    df_final["speechiness_var"] = (0.5 - df_final["speechiness"]) ** 2
    df_final["acousticness_var"] = (0.5 - df_final["acousticness"]) ** 2
    df_final["instrumentalness_var"] = (0.5 - df_final["instrumentalness"]) ** 2
    df_final["liveness_var"] = (0.5 - df_final["liveness"]) ** 2
    df_final["valence_var"] = (0.5 - df_final["valence"]) ** 2

    df_final = df_final.sort_values(
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
    print(df_final.head())
    # Play last played song and record signals
    st.write("Playing ...")
    # Spotify line
    st.write("Your brainwaves...")
    # TODO
    """
    df_eeg = neurofeedback.neurofeedback_fn()

    if option_a is True and option_t is False and option_b is False:
        st.write('Creating Calm and Relaxing Vibes')
        if df_eeg.alpha_metrics.quantile([0.75]) - df_eeg.alpha_metrics.quantile([0.25])>0:
            print("Use metrics from the current spotify song to recommend the next song which is similar to the current song")
        elif df_eeg.alpha_metrics.quantile([0.75]) - df_eeg.alpha_metrics.quantile([0.25])<0:
            print("Try next song from the initially made playlist")

    elif option_b is True and option_t is False and option_a is False:
        st.write("Creating High Octane and Adventurous Vibe")
        if df_eeg.beta_metrics.quantile([0.75]) - df_eeg.alpha_metrics.quantile([0.25])>0:
            print("Use metrics from the current spotify song to recommend the next song which is similar to the current song")
        elif df_eeg.beta_metrics.quantile([0.75]) - df_eeg.alpha_metrics.quantile([0.25])<0:
            print("Try next song from the initially made playlist")
    
    elif option_t is True and option_a is False and option_b is False:
        st.write("Creating Focussed Vibe")
        if df_eeg.theta_metrics.quantile([0.75]) - df_eeg.theta_metrics.quantile([0.25])>0:
            print("Use metrics from the current spotify song to recommend the next song which is similar to the current song")
        elif df_eeg.theta_metrics.quantile([0.75]) - df_eeg.theta_metrics.quantile([0.25])<0:
            print("Try next song from the initially made playlist")    

    elif option_a and option_b:
        st.write("This might be messy but generating high octane relaxing music")
        if (df_eeg.alpha_metrics.quantile([0.75]) - df_eeg.alpha_metrics.quantile([0.25])>0) and (df_eeg.beta_metrics.quantile([0.75]) - df_eeg.beta_metrics.quantile([0.25])>0):
            print("Use metrics from the current spotify song to recommend the next song which is similar to the current song")
        else:
            print("Try next song from the initially made playlist")

    elif option_a and option_t:
        st.write("Creating Calm and Focussed Vibes")
        if (df_eeg.alpha_metrics.quantile([0.75]) - df_eeg.alpha_metrics.quantile([0.25])>0) and (df_eeg.theta_metrics.quantile([0.75]) - df_eeg.theta_metrics.quantile([0.25])>0):
            print("Use metrics from the current spotify song to recommend the next song which is similar to the current song")
        else:
            print("Try next song from the initially made playlist")

    elif option_b and option_t:
        st.write("Creating High Energy and Focussed Vibes")
        if (df_eeg.beta_metrics.quantile([0.75]) - df_eeg.beta_metrics.quantile([0.25])>0) and (df_eeg.theta_metrics.quantile([0.75]) - df_eeg.theta_metrics.quantile([0.25])>0):
            print("Use metrics from the current spotify song to recommend the next song which is similar to the current song")
        else:
            print("Try next song from the initially made playlist")

    elif option_a and option_b and option_t:
        st.write("Creating Mixed Playlist")
        if (df_eeg.alpha_metrics.quantile([0.75]) - df_eeg.alpha_metrics.quantile([0.25])>0) and (df_eeg.beta_metrics.quantile([0.75]) - df_eeg.beta_metrics.quantile([0.25])>0) and (df_eeg.theta_metrics.quantile([0.75]) - df_eeg.theta_metrics.quantile([0.25])>0):
            print("Use metrics from the current spotify song to recommend the next song which is similar to the current song")
        else:
            print("Try next song from the initially made playlist")
    
    else:
        st.write("Creating Mixed Playlist")
        # No Sorting
    """
if col2.button("Stop"):
    # This would empty everything inside the container
    placeholder.empty()
