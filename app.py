# src/app.py
import streamlit as st
import os
import chardet
import tempfile
from src.data_loader import load_data
from src.trend_analysis import trend_analysis
from src.artist_impact import artist_impact
from src.playlist_influence import playlist_influence
from src.external_factors import external_factors
from src.ml_model import train_model, predict_popularity
from src.recommendation_system import create_embeddings, get_recommendations
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_lottie import st_lottie
import json

st.set_page_config(layout="wide", page_title="Spotify 2024 Analysis")

# # Load custom CSS from the 'assets/styles.css' file
# with open('assets/styles.css') as f:
#     css = f.read()
#
# # Inject custom CSS
# st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Load Lottie animation
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_spotify = load_lottie_file("assets/images/spotify.json")

# Display title with Spotify Lottie animation
col1, col2 = st.columns([1, 9])
with col1:
    st_lottie(lottie_spotify, height=50, width=50, key="spotify_title")
with col2:
    st.title("Spotify 2024 Top Streamed Songs")

st.markdown("Analyze the trends, artist impacts, playlist influences, and external factors for the top streamed songs on Spotify in 2024.")

# Load data
@st.cache_data
def load_cached_data():
    data = load_data("data/spotify_2024_top_streamed.csv")
    data['Release Date'] = pd.to_datetime(data['Release Date'])
    return data

data = load_cached_data()

# Create embeddings for the dataset
@st.cache_resource
def get_cached_embeddings(data):
    return create_embeddings(data)

song_embeddings = get_cached_embeddings(data)

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
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
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
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Trend Analysis", "Artist Impact", "Playlist Influence", "External Factors", "Popularity Predictor", "Recommendation System"])

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
            st.header("Song Recommendation System")

            st.subheader("Get recommendations based on a song")
            query_song = st.text_input("Enter a song name (e.g., 'Shape of You by Ed Sheeran')")

            if st.button("Get Recommendations"):
                if query_song:
                    recommendations = get_recommendations(query_song, data, song_embeddings)
                    st.write("Recommended Songs:")
                    st.dataframe(recommendations[['Track', 'Artist', 'Album Name', 'Release Date']])
                else:
                    st.warning("Please enter a song name.")

            st.subheader("Upload Your Spotify Playlist")
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
                        allow_unsafe_jscode=True,
                    )

                    # Get the updated dataframe
                    updated_df = grid_response['data']

                    if st.button("Get Recommendations Based on Your Playlist"):
                        all_recommendations = pd.DataFrame()
                        for _, row in updated_df.iterrows():
                            query = f"{row['Track']} by {row['Artist']}"
                            recommendations = get_recommendations(query, data, song_embeddings, n=2)
                            all_recommendations = pd.concat([all_recommendations, recommendations])

                        all_recommendations = all_recommendations.drop_duplicates(subset=['Track', 'Artist'])
                        st.write("Recommended Songs Based on Your Playlist:")
                        st.dataframe(all_recommendations[['Track', 'Artist', 'Album Name', 'Release Date']])

                    # Close and delete the temporary file after use
                    os.remove(temp_filename)

                except Exception as e:
                    st.error(f"Error processing the uploaded file: {str(e)}")
                    st.error("Please ensure your CSV file is properly formatted and contains the required columns.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Footer section with lottie animations
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Load Lottie animations
lottie_github = load_lottie_file("assets/images/github.json")
lottie_linkedin = load_lottie_file("assets/images/linkedin.json")
lottie_portfolio = load_lottie_file("assets/images/portfolio.json")

st.markdown(
    """
    <div style='text-align: center;'>
        <h3>Made with ❤️ by Mebarek</h3>
        <p>Connect with me:</p>
    </div>
    """, unsafe_allow_html=True
)

# Display Lottie animations and social media links side by side
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st_lottie(lottie_github, height=50, width=50, key="lottie_github")
with col2:
    st.markdown("<a href='https://github.com/Mohammed-Mebarek-Mecheter/' target='_blank'>GitHub</a>", unsafe_allow_html=True)

with col3:
    st_lottie(lottie_linkedin, height=50, width=50, key="lottie_linkedin")
with col4:
    st.markdown("<a href='https://www.linkedin.com/in/mohammed-mecheter/' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)

with col5:
    st_lottie(lottie_portfolio, height=50, width=50, key="lottie_portfolio")
with col6:
    st.markdown("<a href='https://mebarek.pages.dev/' target='_blank'>Portfolio</a>", unsafe_allow_html=True)

st.markdown(
    """
    <div style='text-align: center;'>
        <p>Data source: <a href="https://datainmotion.co">Data in Motion</a> | Last updated: August 02, 2024</p>
    </div>
    """, unsafe_allow_html=True
)