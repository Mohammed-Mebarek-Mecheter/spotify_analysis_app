# src/external_factors.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def external_factors(data):
    st.header("External Factors")

    # Correlation with Streaming Counts using Plotly
    st.subheader("Correlation with Streaming Counts")
    external_factors = data[['Shazam Counts', 'SiriusXM Spins', 'Spotify Streams', 'Explicit Track']]
    corr = external_factors.corr()

    heatmap = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='greens'
    ))

    heatmap.update_layout(
        width=700,
        height=400,
        title="Correlation with Streaming Counts"
    )

    st.plotly_chart(heatmap, use_container_width=True)

    # Box Plot of Explicit vs. Non-Explicit Streams using Plotly
    st.subheader("Explicit vs. Non-Explicit Streams")
    box_plot = px.box(
        data,
        x='Explicit Track',
        y='Spotify Streams',
        title="Explicit vs. Non-Explicit Streams",
        labels={'Explicit Track': 'Explicit Track', 'Spotify Streams': 'Spotify Streams'},
        width=700,
        height=400
    )

    st.plotly_chart(box_plot, use_container_width=True)

    # Scatter Plot of Shazam Counts vs. Stream Counts using Plotly
    st.subheader("Shazam Counts vs. Stream Counts")
    scatter_plot = px.scatter(
        data,
        x='Shazam Counts',
        y='Spotify Streams',
        color='Explicit Track',
        title="Shazam Counts vs. Stream Counts",
        labels={'Shazam Counts': 'Shazam Counts', 'Spotify Streams': 'Spotify Streams', 'Explicit Track': 'Explicit Track'},
        size_max=60,
        width=700,
        height=400
    )

    st.plotly_chart(scatter_plot, use_container_width=True)
