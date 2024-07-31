# src/playlist_influence.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def playlist_influence(data):
    st.header("Playlist Influence")

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    playlist_features = data[['Spotify Playlist Count', 'Spotify Playlist Reach', 'YouTube Playlist Reach', 'Apple Music Playlist Count', 'Deezer Playlist Count', 'Amazon Playlist Count', 'Spotify Streams']]
    corr = playlist_features.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # Top Playlists by Contribution to Streams
    st.subheader("Top Playlists by Contribution to Streams")
    top_playlists = data[['Spotify Playlist Count', 'Spotify Streams']].groupby('Spotify Playlist Count').sum().sort_values(by='Spotify Streams', ascending=False).head(10)
    st.bar_chart(top_playlists)
