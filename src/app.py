# src/app.py
import streamlit as st
from data_loader import load_data
import tempfile
import os
from trend_analysis import trend_analysis
from artist_impact import artist_impact
from playlist_influence import playlist_influence
from external_factors import external_factors
from ml_model import train_model, predict_popularity
import pandas as pd
from datetime import datetime
import chardet
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(layout="wide", page_title="Spotify 2024 Analysis")

st.title("Spotify 2024 Top Streamed Songs Analysis")
st.markdown("Analyze the trends, artist impacts, playlist influences, and external factors for the top streamed songs on Spotify in 2024.")

# Load data
@st.cache_data
def load_cached_data():
    return load_data("data/spotify_2024_top_streamed.csv")

data = load_cached_data()

# Sidebar for filters
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Year", options=[2024])
artist = st.sidebar.text_input("Artist")
date_range = st.sidebar.date_input("Select Date Range", [])

# Filter data based on user input
def filter_data(df, year=None, artist=None, start_date=None, end_date=None):
    filtered_df = df.copy()

    if year:
        filtered_df = filtered_df[filtered_df['Release Date'].dt.year == year]

    if artist:
        filtered_df = filtered_df[filtered_df['Artist'].str.contains(artist, case=False, na=False)]

    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Release Date'] >= start_date) & (filtered_df['Release Date'] <= end_date)]

    return filtered_df

# Apply filters and handle errors
try:
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        if start_date > end_date:
            st.sidebar.error("Start date must be before end date.")
            filtered_data = data
        else:
            filtered_data = filter_data(data, year=year, artist=artist, start_date=start_date, end_date=end_date)
    else:
        filtered_data = filter_data(data, year=year, artist=artist)

    if artist and filtered_data.empty:
        st.sidebar.warning(f"No data found for artist: {artist}. Showing all data.")
        filtered_data = data

    if filtered_data.empty:
        st.warning("No data available for the selected filters. Please adjust your selection.")
    else:
        # Tabs for different analyses
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Trend Analysis", "Artist Impact", "Playlist Influence", "External Factors", "Popularity Predictor", "Upload Playlist"])

        with tab1:
            trend_analysis(filtered_data)

        with tab2:
            artist_impact(filtered_data)

        with tab3:
            playlist_influence(filtered_data)

        with tab4:
            external_factors(filtered_data)

        with tab5:
            st.header("Song Popularity Predictor")

            model, rmse, feature_names = train_model(data)
            st.markdown(f"**Model RMSE:** {rmse:.2f}")

            st.subheader("Predict the popularity of a song")
            spotify_playlist_count = st.number_input("Spotify Playlist Count", min_value=0, max_value=100, value=10)
            spotify_playlist_reach = st.number_input("Spotify Playlist Reach", min_value=0, max_value=1_000_000, value=100_000)
            youtube_playlist_reach = st.number_input("YouTube Playlist Reach", min_value=0, max_value=1_000_000, value=50_000)
            apple_music_playlist_count = st.number_input("Apple Music Playlist Count", min_value=0, max_value=100, value=5)
            siriusxm_spins = st.number_input("SiriusXM Spins", min_value=0, max_value=1000, value=100)
            deezer_playlist_count = st.number_input("Deezer Playlist Count", min_value=0, max_value=100, value=3)
            amazon_playlist_count = st.number_input("Amazon Playlist Count", min_value=0, max_value=100, value=2)
            shazam_counts = st.number_input("Shazam Counts", min_value=0, max_value=1_000_000, value=5000)
            explicit_track = st.selectbox("Explicit Track", options=[False, True])

            features = {
                'Spotify Playlist Count': spotify_playlist_count,
                'Spotify Playlist Reach': spotify_playlist_reach,
                'YouTube Playlist Reach': youtube_playlist_reach,
                'Apple Music Playlist Count': apple_music_playlist_count,
                'SiriusXM Spins': siriusxm_spins,
                'Deezer Playlist Count': deezer_playlist_count,
                'Amazon Playlist Count': amazon_playlist_count,
                'Shazam Counts': shazam_counts,
                'Explicit Track': explicit_track
            }

            if st.button("Predict Popularity"):
                prediction = predict_popularity(model, features, feature_names)
                st.markdown(f"**Predicted Spotify Streams:** {prediction:.0f}")

        with tab6:
            st.header("Upload Your Spotify Playlist")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_filename = temp_file.name

            # Detect the file encoding
            with open(temp_filename, 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']

            # Read the CSV file with the detected encoding
            user_playlist = pd.read_csv(temp_filename, encoding=encoding)

            # Create an editable AgGrid
            gb = GridOptionsBuilder.from_dataframe(user_playlist)
            gb.configure_default_column(editable=True, groupable=True)
            grid_options = gb.build()

            grid_response = AgGrid(
                user_playlist,
                gridOptions=grid_options,
                height=400,
                width='100%',
                data_return_mode='AS_INPUT',
                update_mode=GridUpdateMode.MODEL_CHANGED,
                fit_columns_on_grid_load=False,
                allow_unsafe_jscode=True,  # Set it to True to allow jsfunction to be injected
            )

            # Get the updated dataframe
            updated_df = grid_response['data']

            # Placeholder for recommendation system based on user playlist analysis
            st.markdown("Recommendation System is under development.")
            # Close and delete the temporary file after use
            os.remove(temp_filename)
        except Exception as e:
            st.error(f"Error reading the uploaded file: {str(e)}")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.error("Please try again with different inputs or refresh the page.")
