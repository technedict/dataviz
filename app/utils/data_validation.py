import os
import pandas as pd

def validate_file(file) -> bool:
    ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
    
    # Check if the file has an allowed extension
    if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
        return False
    
    try:
        # Try reading the file with pandas to check for read errors
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Perform additional checks, such as verifying column names, data types, etc.
        # Example: Check if required columns exist
        # required_columns = ['column1', 'column2']
        # if not all(col in df.columns for col in required_columns):
        #     return False
        
        return True
    except Exception:
        return False
