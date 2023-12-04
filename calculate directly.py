import pandas as pd
import math
from statistics import median
import numpy as np

def read_numeric_column_from_excel(file_path: str, sheet_name: str, column_name: str) -> list:
    """
    Reads data from an Excel file and extracts a specific column as a list,
    filtering out non-numeric values.

    Parameters:
    - file_path (str): The path to the Excel file.
    - sheet_name (str): The name of the sheet containing the data.
    - column_name (str): The name of the column to extract.

    Returns:
    list: A list containing only the numeric values from the specified column.

    Raises:
    - FileNotFoundError: If the specified file path does not exist.
    - ValueError: If the specified sheet name or column name does not exist in the Excel file.
    - TypeError: If the data in the specified column cannot be converted to numeric values.
    """

    try:
        # Read the Excel file and extract the specified sheet
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # Check if the specified column exists in the sheet
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' does not exist in sheet '{sheet_name}'.")

        # Filter out non-numeric values from the specified column
        numeric_column = df[column_name].loc[pd.to_numeric(df[column_name], errors='coerce').notnull()]

        # Convert the filtered column to a list
        numeric_list = numeric_column.tolist()

        # Return the resulting numeric list
        return numeric_list

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")

    except ValueError as e:
        raise ValueError(str(e))

    except TypeError:
        raise TypeError(f"Data in column '{column_name}' cannot be converted to numeric values.")

# Example usage:

# Read numeric values from 'Sheet2' in 'data.xlsx' file, column 'A'
file_path = 'data.xlsx'
sheet_name = 'Sheet1'

e_hbO2_660 = 320
e_hb_660 = 3200
e_hbO2_810 = 860
e_hb_810 = 880
e_hbO2_940 = 1200
e_hb_940 = 800

# Air and sample measurements for red and NIR wavelengths
air_660 = median(read_numeric_column_from_excel(file_path, sheet_name, 'air_660'))
clear_660 = median(read_numeric_column_from_excel(file_path, sheet_name, 'Sam1_660'))
red_660 = median(read_numeric_column_from_excel(file_path, sheet_name, 'Sam2_660'))

air_810 = median(read_numeric_column_from_excel(file_path, sheet_name, 'air_810'))
clear_810 = median(read_numeric_column_from_excel(file_path, sheet_name, 'Sam1_810'))
red_810 = median(read_numeric_column_from_excel(file_path, sheet_name, 'Sam2_810'))

air_940 = median(read_numeric_column_from_excel(file_path, sheet_name, 'air_940'))
clear_940 = median(read_numeric_column_from_excel(file_path, sheet_name, 'Sam1_940'))
red_940 = median(read_numeric_column_from_excel(file_path, sheet_name, 'Sam2_940'))

# Calculation of absorbances
A_red1 = math.log10(air_660/clear_660)
A_nir1 = math.log10(air_810/clear_810)
A_Nir1 = math.log10(air_940/clear_940)
A_red2 = math.log10(air_660/red_660)
A_nir2 = math.log10(air_810/red_810)
A_Nir2 = math.log10(air_940/red_940)

# ISOSBESTIC METHOD
R1_810 = A_red1 / A_nir1
R2_810 = A_red2 / A_nir2

R1_940 = A_red1 / A_Nir1
R2_940 = A_red2 / A_Nir2

# ScvO2 calculations with 660nm and 810nm
ScvO2_1_810 = (e_hb_660 - R1_810 * e_hb_810) / (e_hb_660 - e_hbO2_660 + R1_810 * (e_hbO2_810 - e_hb_810)) * 100
ScvO2_2_810 = (e_hb_660 - R2_810 * e_hb_810) / (e_hb_660 - e_hbO2_660 + R2_810 * (e_hbO2_810 - e_hb_810)) * 100

# ScvO2 calculations with 660nm and 940nm
ScvO2_1_940 = (e_hb_660 - R1_940 * e_hb_940) / (e_hb_660 - e_hbO2_660 + R1_940 * (e_hbO2_940 - e_hb_940)) * 100
ScvO2_2_940 = (e_hb_660 - R2_940 * e_hb_940) / (e_hb_660 - e_hbO2_660 + R2_940 * (e_hbO2_940 - e_hb_940)) * 100

print(f'ScvO2 (w/ 660nm and 810nm) of sample 1 = {round(ScvO2_1_810, 2)}%')
print(f'ScvO2 (w/ 660nm and 810nm) of sample 2 = {round(ScvO2_2_810, 2)}%')
print(f'ScvO2 (w/ 660nm and 940nm) of sample 1 = {round(ScvO2_1_940, 2)}%')
print(f'ScvO2 (w/ 660nm and 940nm) of sample 2 = {round(ScvO2_2_940, 2)}%')


