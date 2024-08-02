# tests/test_data_loader.py

import pytest
import pandas as pd
from src.data_loader import load_data

@pytest.fixture
def mock_csv(tmp_path):
    df = pd.DataFrame({
        'Artist': ['Artist1', 'Artist2'],
        'Track': ['Track1', 'Track2'],
        'Release Date': ['2024-01-01', '2024-02-01'],
        'Spotify Streams': [1000, 2000]
    })
    csv_file = tmp_path / "test_data.csv"
    df.to_csv(csv_file, index=False)
    return csv_file

def test_load_data(mock_csv):
    data = load_data(mock_csv)
    assert isinstance(data, pd.DataFrame)
    assert len(data) == 2
    assert 'Release Date' in data.columns
    assert pd.api.types.is_datetime64_any_dtype(data['Release Date'])