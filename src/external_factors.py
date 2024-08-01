# src/external_factors.py

import streamlit as st
import pandas as pd
import altair as alt

def external_factors(data):
    st.header("External Factors")

    # Correlation with Streaming Counts using Altair
    st.subheader("Correlation with Streaming Counts")
    external_factors = data[['Shazam Counts', 'SiriusXM Spins', 'Spotify Streams', 'Explicit Track']]
    corr = external_factors.corr().reset_index().melt('index')
    corr.columns = ['Feature1', 'Feature2', 'Correlation']

    heatmap = alt.Chart(corr).mark_rect().encode(
        x='Feature1:O',
        y='Feature2:O',
        color='Correlation:Q',
        tooltip=['Feature1:O', 'Feature2:O', 'Correlation:Q']
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(heatmap, use_container_width=True)

    # Box Plot of Explicit vs. Non-Explicit Streams using Altair
    st.subheader("Explicit vs. Non-Explicit Streams")
    box_plot = alt.Chart(data).mark_boxplot().encode(
        x='Explicit Track:N',
        y='Spotify Streams:Q',
        tooltip=['Explicit Track:N', 'Spotify Streams:Q']
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(box_plot, use_container_width=True)

    # Scatter Plot of Shazam Counts vs. Stream Counts using Altair
    st.subheader("Shazam Counts vs. Stream Counts")
    scatter_plot = alt.Chart(data).mark_circle(size=60).encode(
        x='Shazam Counts:Q',
        y='Spotify Streams:Q',
        color='Explicit Track:N',
        tooltip=['Shazam Counts:Q', 'Spotify Streams:Q', 'Explicit Track:N']
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(scatter_plot, use_container_width=True)
