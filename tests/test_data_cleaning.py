import pytest
import pandas as pd
from app.utils.data_cleaning import clean_data

def test_clean_data():
    df = pd.DataFrame({
        'A': [1, 2, 2, 3, None],
        'B': [1, 2, 2, 3, 4],
        'C': [1.5, 2.5, 2.5, 3.5, 4.5]
    })
    
    cleaned_df = clean_data(df, remove_na=True, remove_duplicates=True, normalize_data=True)
    
    assert cleaned_df.isnull().sum().sum() == 0  # No missing values
    assert len(cleaned_df) == 3  # After removing NA and duplicates
    assert cleaned_df['A'].mean() == 0  # Mean of normalized data should be 0
