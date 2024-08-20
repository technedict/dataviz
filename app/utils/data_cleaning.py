import pandas as pd
import json
import csv
from sklearn.preprocessing import StandardScaler

def clean_data(df: pd.DataFrame, remove_na: bool, remove_duplicates: bool, normalize_data: bool) -> pd.DataFrame:
    # Handle missing values
    if remove_na:
        df = df.dropna()
    
    # Remove duplicate rows
    if remove_duplicates:
        df = df.drop_duplicates()
    
    # Normalize numerical data
    if normalize_data:
        numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
        scaler = StandardScaler()
        df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
    
    # Convert DataFrame to JSON only after all operations are done
    df_json = df.to_json(orient='records')

    return df_json

def save_json_to_csv(json_string, csv_file_path):

    try:
        # Parse the JSON string into a Python object (usually a list of dictionaries)
        data = json.loads(json_string)

        # Check if the data is a list (list of dictionaries)
        if isinstance(data, list):
            # If the list is not empty, proceed to save as CSV
            if len(data) > 0:
                # Get the headers from the keys of the first dictionary
                headers = data[0].keys()

                # Write the data to a CSV file
                with open(csv_file_path, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(data)
                print(f"Data successfully saved to {csv_file_path}")

            else:
                print("JSON list is empty, no data to save.")
        
        else:
            print("JSON data is not a list of dictionaries.")
    
    except json.JSONDecodeError:
        print("Invalid JSON string.")
