import streamlit as st
import time
import numpy as np
import datetime

st.set_page_config(page_title="Mood Switch", page_icon="📈")

st.markdown("# Mood Switch")
st.sidebar.header("Mood Switch")
st.write(
    """Here you can set the vibe of your travel plans"""
)

if st.button("Start Playing Vybey Music"):
    st.write("Playing ...")
    st.write("Your brainwaves...")
    #time.sleep(10)
