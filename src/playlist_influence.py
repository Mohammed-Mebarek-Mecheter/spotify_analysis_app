# src/playlist_influence.py

import streamlit as st
import pandas as pd
import altair as alt

def playlist_influence(data):
    st.header("Playlist Influence")

    # Correlation Heatmap using Altair
    st.subheader("Correlation Heatmap")
    playlist_features = data[['Spotify Playlist Count', 'Spotify Playlist Reach', 'YouTube Playlist Reach', 'Apple Music Playlist Count', 'Deezer Playlist Count', 'Amazon Playlist Count', 'Spotify Streams']]
    corr = playlist_features.corr().reset_index().melt('index')
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

    # Top Playlists by Contribution to Streams using Altair
    st.subheader("Top Playlists by Contribution to Streams")
    top_playlists = data.groupby('Spotify Playlist Count')['Spotify Streams'].sum().reset_index().sort_values(by='Spotify Streams', ascending=False).head(10)

    bar_chart = alt.Chart(top_playlists).mark_bar().encode(
        x='Spotify Streams:Q',
        y=alt.Y('Spotify Playlist Count:Q', sort='-x'),
        tooltip=['Spotify Playlist Count:Q', 'Spotify Streams:Q']
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(bar_chart, use_container_width=True)
