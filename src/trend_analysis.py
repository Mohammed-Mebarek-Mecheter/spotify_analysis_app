# src/trend_analysis.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def trend_analysis(data):
    st.header("Trend Analysis")

    # Time Series Chart
    st.subheader("Song Releases Over Time")
    monthly_releases = data['Release Date'].dt.to_period('M').value_counts().sort_index()
    st.line_chart(monthly_releases)

    # Heatmap by Month and Day of Week
    st.subheader("Heatmap of Song Releases")
    data['Month'] = data['Release Date'].dt.month
    data['Day of Week'] = data['Release Date'].dt.dayofweek
    heatmap_data = data.pivot_table(index='Month', columns='Day of Week', values='Track', aggfunc='count')
    fig, ax = plt.subplots()
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f', ax=ax)
    st.pyplot(fig)

    # Seasonal Trend Analysis (Decomposition)
    st.subheader("Seasonal Trend Analysis")
    st.markdown("Currently not implemented. Placeholder for future decomposition plots.")
