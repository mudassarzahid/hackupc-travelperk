import datetime
import seaborn as sns

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Streamlit UI
st.title('Title')

# User inputs
date_input = st.date_input(
    "Select day",
    value=[datetime.date(2024, 5, 5), datetime.date(2024, 5, 5)],
    min_value=datetime.date.today(),
)
