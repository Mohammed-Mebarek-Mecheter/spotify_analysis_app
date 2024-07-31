# src/external_factors.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def external_factors(data):
    st.header("External Factors")

    # Correlation with Streaming Counts
    st.subheader("Correlation with Streaming Counts")
    external_factors = data[['Shazam Counts', 'SiriusXM Spins', 'Spotify Streams', 'Explicit Track']]
    corr = external_factors.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # Box Plot of Explicit vs. Non-Explicit Streams
    st.subheader("Explicit vs. Non-Explicit Streams")
    fig, ax = plt.subplots()
    sns.boxplot(x='Explicit Track', y='Spotify Streams', data=data, ax=ax)
    st.pyplot(fig)

    # Scatter Plot of Shazam Counts vs. Stream Counts
    st.subheader("Shazam Counts vs. Stream Counts")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Shazam Counts', y='Spotify Streams', data=data, ax=ax)
    st.pyplot(fig)
