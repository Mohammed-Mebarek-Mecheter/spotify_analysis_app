# Spotify 2024 Top Streamed Songs Analysis

## Overview

This Streamlit app is designed to analyze the trends and characteristics of the most streamed songs on Spotify in 2024. The goal is to enhance user experience, improve recommendations, and optimize playlist curation by uncovering key factors contributing to high stream counts. This app provides actionable insights for marketing and curation teams, ultimately enhancing user engagement through improved recommendations and playlist curation.

Check out the live app: [Spotify Analysis App](https://spotify-music.streamlit.app/)

## Features and Components

### 1. Elegant and Impressive Design
- **Wide Layout**: Better visualization on larger screens.
- **Consistent Color Scheme**: Clean, modern design.
- **Built-in Components**: Polished look using Streamlit's built-in components.
- **Animations and Transitions**: Dynamic feel with animations.

### 2. Features and Components.

#### a. Sidebar
- Include filters for year, artist, and date range.

#### b. Trend Analysis Tab
- Interactive time series chart showing song releases over time.
- Heatmap of song releases by month and day of the week.
- Placeholder for seasonal trend analysis with decomposition plots.

#### c. Artist Impact Tab
- Bar chart of top artists by average streams.
- Scatter plot of artist popularity vs. stream counts.

#### d. Playlist Influence Tab
- Correlation heatmap between playlist features and stream counts.
- Bar chart of top playlists by contribution to streams.

#### e. External Factors Tab
- Correlation analysis between external factors and stream counts.
- Box plots comparing explicit vs. non-explicit content streams.
- Scatter plot of Shazam counts vs. stream counts.

#### f. Popularity Predictor Tab
- Simple prediction model for song popularity based on its features.
- Users can input song characteristics and get a predicted stream count.

#### g. Recommendation System Tab
- Users can upload their own Spotify playlist for analysis.
- Recommendation system based on the analysis of the uploaded playlist.

### 3. Interactive Elements
- Tooltips for detailed information on hover.
- Sliders or multi-select dropdowns for filtering data.
- Clickable elements that update other visualizations.

### 4. Performance Optimization
- Caching for data loading and heavy computations.
- Lazy loading for charts and graphs.

### 5. Responsive Design
- Ensure the app looks good on both desktop and mobile devices.
- Use Streamlit's column layout for better organization on different screen sizes.

## Setup Instructions

### 1. Prerequisites
- Python 3.7 or higher
- Git (optional, for cloning the repository)

### 2. Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Mohammed-Mebarek-Mecheter/spotify_analysis_app.git
   cd spotify_analysis_app
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run src/app.py
   ```

## Acknowledgment

This app was developed using the dataset provided by [Data in Motion](https://datainmotion.co) as part of their weekly challenges. Special thanks to Data in Motion for their valuable resources and support.

## Project Structure

```plaintext
spotify_analysis_app/
├── .gitignore
├── assets/
│   ├── images/
│   │   ├── .gif
│   │   ├── .json
│   │   ├── ...
│   ├── styles.css
├── data/
│   ├── spotify_2024_top_streamed.csv
├── README.md
├── requirements.txt
├── setup.sh
├── src/
│   ├── app.py
│   ├── artist_impact.py
│   ├── data_loader.py
│   ├── external_factors.py
│   ├── ml_model.py
│   ├── playlist_influence.py
│   ├── recommendation_system.py
│   ├── trend_analysis.py
│   ├── __init__.py
```

## Files Description

### `assets/`
- **styles.css**: Custom CSS for styling the app.
- **images/**: Contains Lottie animations for enhancing UI.

### `data/`
- **spotify_2024_top_streamed.csv**: Dataset containing detailed information about the top streamed songs on Spotify in 2024.

### `src/`
- **app.py**: Main script to run the Streamlit app.
- **artist_impact.py**: Script for the artist impact tab.
- **data_loader.py**: Script for loading and preprocessing the data.
- **external_factors.py**: Script for the external factors tab.
- **ml_model.py**: Script for training and predicting song popularity using a machine learning model.
- **playlist_influence.py**: Script for the playlist influence tab.
- **recommendation_system.py**: Script for the recommendation system.
- **trend_analysis.py**: Script for the trend analysis tab.

### `setup.sh`
- Shell script to set up the environment (e.g., installing dependencies).

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run src/app.py
   ```

2. Use the sidebar to filter data by year, artist, and date range.

3. Navigate through the tabs to explore different analyses and insights:
    - **Trend Analysis**: View trends in song releases.
    - **Artist Impact**: Analyze the impact of artists on streaming counts.
    - **Playlist Influence**: Assess the influence of playlist inclusion on streaming counts.
    - **External Factors**: Investigate how external factors affect song popularity.
    - **Popularity Predictor**: Predict song popularity based on its features.
    - **Recommendation System**: Upload your own Spotify playlist and get song recommendations.

## Contact

For any questions or feedback, please reach out to the developer:

- **GitHub**: [Mohammed-Mebarek-Mecheter](https://github.com/Mohammed-Mebarek-Mecheter/)
- **LinkedIn**: [mohammed-mecheter](https://www.linkedin.com/in/mohammed-mecheter/)
- **Portfolio**: [Mebarek](https://mebarek.pages.dev/)

## License

This project is licensed under the MIT License.
