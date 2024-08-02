# src/playlist_influence.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

def playlist_influence(data):
    st.header("Playlist Influence")

    # Correlation Heatmap using Plotly
    st.subheader("Correlation Heatmap")
    playlist_features = data[['Spotify Playlist Count', 'Spotify Playlist Reach', 'YouTube Playlist Reach', 'Apple Music Playlist Count', 'Deezer Playlist Count', 'Amazon Playlist Count', 'Spotify Streams']]
    corr = playlist_features.corr()

    heatmap = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='greens'
    ))

    heatmap.update_layout(
        width=700,
        height=400,
        title="Correlation Heatmap"
    )

    st.plotly_chart(heatmap, use_container_width=True)

    # Top Playlists by Contribution to Streams using Altair
    st.subheader("Top Playlists by Contribution to Streams")
    top_playlists = data.groupby('Spotify Playlist Count')['Spotify Streams'].sum().reset_index().sort_values(by='Spotify Streams', ascending=False).head(10)

    bar_chart = alt.Chart(top_playlists).mark_bar().encode(
        x='Spotify Streams:Q',
        y=alt.Y('Spotify Playlist Count:Q', sort='-x'),
        tooltip=['Spotify Playlist Count:Q', 'Spotify Streams:Q']
    ).properties(
        width=700,
        height=400,
    )
    st.altair_chart(bar_chart, use_container_width=True)
