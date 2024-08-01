# src/artist_impact.py

import streamlit as st
import pandas as pd
import altair as alt

def artist_impact(data):
    st.header("Artist Impact")

    # Top Artists by Average Streams using Altair
    st.subheader("Top Artists by Average Streams")
    top_artists = data.groupby('Artist')['Spotify Streams'].mean().sort_values(ascending=False).head(10).reset_index()

    bar_chart = alt.Chart(top_artists).mark_bar().encode(
        x='Spotify Streams:Q',
        y=alt.Y('Artist:N', sort='-x'),
        tooltip=['Artist:N', 'Spotify Streams:Q']
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(bar_chart, use_container_width=True)

    # Scatter Plot of Artist Popularity vs. Stream Counts using Altair
    st.subheader("Artist Popularity vs. Stream Counts")
    artist_popularity = data.groupby('Artist').agg({'Spotify Streams': 'sum', 'Track': 'count'}).reset_index()
    artist_popularity.columns = ['Artist', 'Total Streams', 'Number of Songs']

    scatter_plot = alt.Chart(artist_popularity).mark_circle(size=60).encode(
        x='Number of Songs:Q',
        y='Total Streams:Q',
        color='Artist:N',
        tooltip=['Artist:N', 'Number of Songs:Q', 'Total Streams:Q']
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(scatter_plot, use_container_width=True)
