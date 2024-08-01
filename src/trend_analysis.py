# src/trend_analysis.py

import streamlit as st
import pandas as pd
import altair as alt

def trend_analysis(data):
    st.header("Trend Analysis")

    # Time Series Chart using Altair
    st.subheader("Song Releases Over Time")
    monthly_releases = data['Release Date'].dt.to_period('M').value_counts().sort_index().reset_index()
    monthly_releases.columns = ['Month', 'Count']
    monthly_releases['Month'] = monthly_releases['Month'].dt.strftime('%Y-%m')

    line_chart = alt.Chart(monthly_releases).mark_line().encode(
        x='Month:T',
        y='Count:Q',
        tooltip=['Month:T', 'Count:Q']
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(line_chart, use_container_width=True)

    # Heatmap by Month and Day of Week using Altair
    st.subheader("Heatmap of Song Releases")
    data['Month'] = data['Release Date'].dt.month
    data['Day of Week'] = data['Release Date'].dt.dayofweek

    heatmap_data = data.groupby(['Month', 'Day of Week']).size().reset_index(name='Count')

    heatmap = alt.Chart(heatmap_data).mark_rect().encode(
        x='Day of Week:O',
        y='Month:O',
        color='Count:Q',
        tooltip=['Month:O', 'Day of Week:O', 'Count:Q']
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(heatmap, use_container_width=True)
