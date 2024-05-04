import io
import os

import spotipy
import streamlit as st
import time
import numpy as np
import datetime

from spotipy import SpotifyOAuth

import neurofeedback
import pandas as pd

os.environ["SPOTIPY_CLIENT_ID"] = '2f817bc820e7470dba54223f96f4d945'
os.environ["SPOTIPY_CLIENT_SECRET"] = '8cbb7a3351b74d7cacec0838d768a5ae'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:3001/app'
scope = "user-library-read" #streaming user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private user-read-recently-played user-read-private"

st.set_page_config(page_title="Mood Switch", page_icon="📈")

st.sidebar.header("Mood Switch")
st.markdown("# Mood Switch")
st.write("""Here you can set the vibe of your travel plans""")

st.divider()
st.write("What type of Vibe would you like your trip to be?")
option_a = st.checkbox('Calm and Relaxing')
option_b = st.checkbox('High Energy & Adventurous')
option_t = st.checkbox('Self Exploration and Intellectual')

st.divider()
if st.button("Start Playing Vibey Music"):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    results = sp.current_user_recently_played()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
    # Import user's playlist (Last 100 songs played)
    # df = pd.read_csv("")

    # Play last played song and record signals
    st.write("Playing ...")
    #Spotify line
    st.write("Your brainwaves...")
    # time.sleep(10)
    # neurofeedback.neurofeedback_fn()

    if option_a is True and option_t is False and option_b is False:
        st.write('Creating Calm and Relaxing Vibes')
        # Sort by
    elif option_b is True and option_t is False and option_a is False:
        st.write("Creating High Octane and Adventurous Vibe")
        # Sort by
    elif option_t is True and option_a is False and option_b is False:
        st.write("Creating Focussed Vibe")
        # Sort by
    elif option_a and option_b:
        st.write("This might be messy but generating high octane relaxing music")
        # Sort by
    elif option_a and option_t:
        st.write("Creating Calm and Focussed Vibes")
        # Sort by
    elif option_b and option_t:
        st.write("Creating High Energy and Focussed Vibes")
        # Sort by
    elif option_a and option_b and option_t:
        st.write("Creating Mixed Playlist")
        # Sort by
    else:
        st.write("Creating Mixed Playlist")
        # No Sorting
