import datetime
import seaborn as sns

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Travel Buddy Matching", page_icon="🌍")

st.markdown("# Travel Buddy Matching")
st.sidebar.header("Travel Buddy Matching")
st.write(
    """Here you can find travel buddies that match your vibe!"""
)

# User inputs
date_input = st.date_input(
    "Select day",
    value=[datetime.date(2024, 5, 5), datetime.date(2024, 5, 5)],
    min_value=datetime.date.today(),
)
