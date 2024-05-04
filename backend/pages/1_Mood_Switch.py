import io
import os
import streamlit as st
import time
import numpy as np
import datetime
import neurofeedback

st.set_page_config(page_title="Mood Switch", page_icon="📈")

st.sidebar.header("Mood Switch")
st.markdown("# Mood Switch")
st.write(
    """Here you can set the vibe of your travel plans"""
)

st.write("What type of Vibe would you like your trip to be?")
option_a = st.checkbox('Calm and Relaxing')
option_b = st.checkbox('High Octance & Adventurous')
option_t = st.checkbox('Self Exploration and Intellectual')

if st.button("Start Playing Vybey Music"):
    st.write("Playing ...")
    st.write("Your brainwaves...")
    #time.sleep(10)
    #neurofeedback.neurofeedback_fn()
    