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

# Initialize the line chart with 0
def init_chart():
    chart_data = pd.DataFrame(np.zeros((1, 3)), columns=["alpha", "beta", "gamma"])
    chart = st.line_chart(chart_data)
    return chart

# update the line chart with new data
def update_line_chart(chart, new_data):
    new_data = pd.DataFrame([new_data], columns=["alpha", "beta", "gamma"])
    chart.add_rows(new_data)



chart = init_chart()
while True:
    data = generate_data()
    update_line_chart(chart, data)
    time.sleep(1)


update_line_chart(st, generate_data)

