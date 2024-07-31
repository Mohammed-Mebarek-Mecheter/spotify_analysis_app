# src/ml_model.py

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

@st.cache_data
def train_model(data):
    features = data[['Spotify Playlist Count', 'Spotify Playlist Reach', 'YouTube Playlist Reach',
                     'Apple Music Playlist Count', 'SiriusXM Spins', 'Deezer Playlist Count',
                     'Amazon Playlist Count', 'Shazam Counts', 'Explicit Track']]
    target = data['Spotify Streams']

    # One-hot encoding for categorical variables
    features = pd.get_dummies(features, columns=['Explicit Track'], prefix='Explicit Track')

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)

    return model, rmse, features.columns

def predict_popularity(model, features, feature_names):
    features_df = pd.DataFrame([features])
    features_df = pd.get_dummies(features_df, columns=['Explicit Track'], prefix='Explicit Track')

    # Ensure all columns from training are present
    for col in feature_names:
        if col not in features_df.columns:
            features_df[col] = 0

    # Reorder columns to match training data
    features_df = features_df[feature_names]

    prediction = model.predict(features_df)
    return prediction[0]
