import pandas as pd


def handle_excel_file(file_path):
    """Read an Excel file and return the data."""
    return pd.read_excel(file_path)
