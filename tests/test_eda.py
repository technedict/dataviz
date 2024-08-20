import pytest
import pandas as pd
from app.utils.eda import generate_summary_statistics, generate_visualization

def test_generate_summary_statistics():
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1]
    })
    summary_stats = generate_summary_statistics(df)
    
    assert summary_stats['A']['mean'] == 3
    assert summary_stats['B']['mean'] == 3

def test_generate_visualization():
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1]
    })
    plot = generate_visualization(df, 'scatter', 'A', 'B')
    
    assert plot is not None
    assert isinstance(plot, str)
