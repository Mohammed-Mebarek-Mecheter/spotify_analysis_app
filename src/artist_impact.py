# src/artist_impact.py

import streamlit as st
import pandas as pd
import plotly.express as px

def artist_impact(data):
    st.header("Artist Impact")

    # Top Artists by Average Streams using Plotly
    st.subheader("Top Artists by Average Streams")
    top_artists = data.groupby('Artist')['Spotify Streams'].mean().sort_values(ascending=False).head(10).reset_index()

    bar_chart = px.bar(
        top_artists,
        x='Spotify Streams',
        y='Artist',
        orientation='h',
        title="Top Artists by Average Streams",
        labels={'Spotify Streams': 'Average Spotify Streams'},
        width=700,
        height=400,
    )
    bar_chart.update_traces(marker_color='#1DB954')  # Set the desired color
    st.plotly_chart(bar_chart, use_container_width=True)

    # Scatter Plot of Artist Popularity vs. Stream Counts using Plotly
    st.subheader("Artist Popularity vs. Stream Counts")
    artist_popularity = data.groupby('Artist').agg({'Spotify Streams': 'sum', 'Track': 'count'}).reset_index()
    artist_popularity.columns = ['Artist', 'Total Streams', 'Number of Songs']

    # Scatter plot
    scatter_plot = px.scatter(
        artist_popularity,
        x='Number of Songs',
        y='Total Streams',
        color='Artist',
        title="Artist Popularity vs. Stream Counts",
        labels={'Number of Songs': 'Number of Songs', 'Total Streams': 'Total Spotify Streams'},
        size='Total Streams',
        hover_data=['Artist', 'Number of Songs', 'Total Streams'],
        width=700,
        height=400
    )

    st.plotly_chart(scatter_plot, use_container_width=True)
