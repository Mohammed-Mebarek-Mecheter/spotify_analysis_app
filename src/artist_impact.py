# src/artist_impact.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def artist_impact(data):
    st.header("Artist Impact")

    # Top Artists by Average Streams
    st.subheader("Top Artists by Average Streams")
    top_artists = data.groupby('Artist')['Spotify Streams'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    top_artists.plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # Scatter Plot of Artist Popularity vs. Stream Counts
    st.subheader("Artist Popularity vs. Stream Counts")
    artist_popularity = data.groupby('Artist').agg({'Spotify Streams': 'sum', 'Track': 'count'})
    artist_popularity.columns = ['Total Streams', 'Number of Songs']
    fig, ax = plt.subplots()
    ax.scatter(artist_popularity['Number of Songs'], artist_popularity['Total Streams'])
    ax.set_xlabel("Number of Songs")
    ax.set_ylabel("Total Streams")
    st.pyplot(fig)
