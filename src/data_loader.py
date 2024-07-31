# src/data_loader.py

import pandas as pd
import streamlit as st

@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath, parse_dates=['Release Date'])
    return data
