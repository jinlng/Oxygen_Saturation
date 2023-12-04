import pandas as pd
import math
from statistics import median

def read_excel_columns(file_path: str, sheet_name: str) -> dict:
    """
    Reads data from an Excel file and extracts all columns as lists.

    This function uses the pandas library to read the Excel file and extract all columns.
    The columns are saved in a dictionary where the keys are column names and the values
    are the corresponding lists.

    Parameters:
    - file_path (str): The path to the Excel file.
    - sheet_name (str): The name of the sheet in the Excel file.

    Returns:
    dict: A dictionary where the keys are column names and the values are the corresponding lists.

    Raises:
    - FileNotFoundError: If the specified Excel file does not exist.
    - ValueError: If the specified sheet does not exist in the Excel file.
    """

    try:
        # Read the Excel file using pandas
        excel_file = pd.ExcelFile(file_path)

        # Check if the specified sheet exists in the Excel file
        if sheet_name not in excel_file.sheet_names:
            raise ValueError(f"Sheet '{sheet_name}' does not exist in the Excel file.")

        # Read the sheet
        data_frame = excel_file.parse(sheet_name)

        # Create a dictionary to store column data
        columns = {}

        # Iterate over each column
        for column in data_frame.columns:
            # Extract the column as a list
            columns[column] = data_frame[column].tolist()

        # Return the dictionary of column values
        return columns

    except FileNotFoundError:
        raise FileNotFoundError(f"Excel file '{file_path}' not found.")

# Example usage:
file_path = "data.xlsx"
sheet_name = "Sheet2"

try:
    column_data = read_excel_columns(file_path, sheet_name)
    for column, values in column_data.items():
        print(f"The column '{column}' from sheet '{sheet_name}' in the Excel file '{file_path}' is:")
        print(values)
except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")

air_660 = median(column_data['air_660'])
clear_660 = median(column_data['clear_660'])
red_660 = median(column_data['red_660'])

air_810 = median(column_data['air_810'])
clear_810 = median(column_data['clear_810'])
red_810 = median(column_data['red_810'])

air_940 = median(column_data['air_940'])
clear_940 = median(column_data['clear_940'])
red_940 = median(column_data['red_940'])