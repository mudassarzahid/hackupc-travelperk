import streamlit as st
import numpy as np
import time
import random

# dummpy function to generate data
def generate_data():
    alpha = random.uniform(20.0, 30.0)
    beta = random.uniform(40.0, 60.0)
    gamma = random.uniform(10.0, 15.0)
    return alpha, beta, gamma

# init the line chart
status_text = st.sidebar.empty()
last_rows = np.random.randn(1,3)
chart = st.line_chart(last_rows)

# while loop to update the line chart
while True:
    a,b,c = generate_data()
    new_rows = np.array([[a,b,c]])
    chart.add_rows(new_rows)
    time.sleep(1)
