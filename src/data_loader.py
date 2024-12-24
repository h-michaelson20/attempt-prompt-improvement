import pandas as pd
from pathlib import Path

def load_excel_data():
    """Load the Excel file from data directory"""
    file_path = Path("data/LLM metrics dec 2024.xlsx")
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        raise Exception(f"Error loading Excel file: {e}")

def get_numeric_columns(df):
    """Return numeric columns from dataframe"""
    return df.select_dtypes(include=['float64', 'int64']).columns

def get_categorical_columns(df):
    """Return categorical columns from dataframe"""
    return df.select_dtypes(include=['object']).columns 