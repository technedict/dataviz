import pytest
import pandas as pd
import os
from app.utils.report_generation import generate_pdf_report, generate_excel_report

def test_generate_pdf_report():
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1]
    })
    pdf_path = generate_pdf_report(df)
    
    assert os.path.exists(pdf_path)
    assert pdf_path.endswith('.pdf')

def test_generate_excel_report():
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1]
    })
    excel_path = generate_excel_report(df)
    
    assert os.path.exists(excel_path)
    assert excel_path.endswith('.xlsx')
