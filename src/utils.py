# src/utils.py

import pandas as pd

def filter_data(data, year=None, artist=None, genre=None):
    if year:
        data = data[data['Release Date'].dt.year == year]
    if artist:
        data = data[data['Artist'].str.contains(artist, case=False)]
    if genre:
        data = data[data['Genre'].str.contains(genre, case=False)]
    return data
