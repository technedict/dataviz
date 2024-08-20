import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

def generate_summary_statistics(df: pd.DataFrame) -> dict:
    summary_stats = df.describe(include='all').to_dict()
    return summary_stats

def generate_visualization(df: pd.DataFrame, chart_type: str, column_x: str, column_y: str = None) -> str:
    plt.figure(figsize=(10, 6))
    
    if chart_type == 'histogram':
        sns.histplot(df[column_x], kde=True)
    elif chart_type == 'scatter' and column_y:
        sns.scatterplot(x=df[column_x], y=df[column_y])
    elif chart_type == 'bar':
        sns.barplot(x=df[column_x], y=df[column_y] if column_y else df.index)
    elif chart_type == 'line':
        sns.lineplot(x=df[column_x], y=df[column_y] if column_y else df.index)
    
    # Save plot to a string buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    return string

