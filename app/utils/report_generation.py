from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import os, uuid

def generate_pdf_report(df: pd.DataFrame, filepath) -> str:
    pdf_path = os.path.join(filepath, f'{str(uuid.uuid4())}.pdf')
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont('Helvetica-Bold', 16)
    c.drawString(100, height - 100, "Data Analysis Report")

    # Summary Statistics
    c.setFont('Helvetica', 12)
    y = height - 150
    c.drawString(100, y, "Summary Statistics:")
    y -= 20
    summary_stats = df.describe().to_dict()
    for stat, values in summary_stats.items():
        c.drawString(100, y, f"{stat}: {values}")
        y -= 20
    
    # Add more details as needed (visualizations, etc.)
    
    c.save()
    return pdf_path


def generate_excel_report(df: pd.DataFrame, filepath) -> str:
    excel_path = os.path.join(filepath, f'{str(uuid.uuid4())}.xlsx')
    
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        # Write summary statistics
        df.describe().to_excel(writer, sheet_name='Summary Statistics')
        
        # Add more sheets for different analyses as needed
    
    return excel_path