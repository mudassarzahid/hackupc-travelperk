import io
import os
import streamlit as st
import time
import numpy as np
import datetime
import neurofeedback
import pandas as pd

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
if st.button("Start Playing Vybey Music"):
    #Import user's playlist (Last 100 songs played)
    #df = pd.read_csv("")
    
    #Play last played song and record signals
    st.write("Playing ...")
    st.write("Your brainwaves...")
    #time.sleep(10)
    #neurofeedback.neurofeedback_fn()

    if option_a==True and option_t==False and option_b==False:
        st.write('Creating Calm and Relaxing Vibes')
        #Sort by 
    elif option_b==True and option_t==False and option_a==False:
        st.write("Creating High Octane and Adventurous Vibe")
        #Sort by 
    elif option_t==True and option_a==False and option_b==False:
        st.write("Creating Focussed Vibe")
        #Sort by 
    elif option_a and option_b:
        st.write("This might be messy but generating high octane relaxing music")
        #Sort by 
    elif option_a and option_t:
        st.write("Creating Calm and Focussed Vibes")
        #Sort by 
    elif option_b and option_t:
        st.write("Creating High Energy and Focussed Vibes")
        #Sort by 
    elif option_a and option_b and option_t:
        st.write("Creating Mixed Playlist")
        #Sort by 
    else:
        st.write("Creating Mixed Playlist")
        #No Sorting