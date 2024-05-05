import streamlit as st
import numpy as np
import time
import random
import pandas as pd

# dummpy function to generate data
def generate_data():
    alpha = random.uniform(20.0, 30.0)
    beta = random.uniform(40.0, 60.0)
    gamma = random.uniform(10.0, 15.0)
    return alpha, beta, gamma

# init line chart
chart_data = pd.DataFrame(np.random.randn(1, 3), columns=["alpha", "beta", "gamma"])
chart = st.line_chart(chart_data)

# loop to update data
while True:
    a,b,c = generate_data()
    chart.add_rows(pd.DataFrame([[a,b,c]],columns=["alpha", "beta", "gamma"]))
    time.sleep(1)

