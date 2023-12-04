# ----------------------------------------------------------------------------
# File: <calculate_oxygen_saturation>.py
# Description: <Calculates the oxygen saturation using absorption spectroscopy measurements in red and NIR wavelengths.>
# Author: <LIANG Jingyi>
# Date: <26/09/2023>
# ----------------------------------------------------------------------------

# ------------------------------
# Importing Necessary Libraries
# ------------------------------
import math


def calculate_oxygen_saturation(red_power: float, nir_power: float) -> float:
    """
    Calculates the oxygen saturation using absorption spectroscopy measurements in red and NIR wavelengths.

    Parameters:
    - red_measurement (float): The optical power measurement obtained from the red light source.
    - nir_measurement (float): The optical power measurement obtained from the NIR light source.

    Returns:
    - float:
        The calculated oxygen saturation value.

    Raises:
    - ValueError:
        Raises an error if either red_power or nir_power is negative.

    Formula:
    The oxygen saturation can be calculated using the formula:
    oxygen_saturation = (red_measurement / nir_measurement) * 100

    red_measurement = 10.5
    nir_measurement = 15.2
    oxygen_saturation = calculate_oxygen_saturation(red_measurement, nir_measurement)
    print(f"The oxygen saturation is: {oxygen_saturation}%")
    """
    # Checking if the power measurements are negative
    if red_power < 0 or nir_power < 0:
        raise ValueError("Measurements cannot be negative.")
    # Checking if the power measurements are zero
    if red_power == 0 or nir_power == 0:
        raise ZeroDivisionError("Measurements should not be zero.")


    # Calculating the oxygen saturation using the formula:
    # oxygen_saturation = (red_power - nir_power) / red_power
    oxygen_saturation = (red_power - nir_power) / red_power *100

    return oxygen_saturation


def get_wavelength_option():
    """
    Prompt the user to choose a wavelength option.

    Returns:
    int: The user's choice of wavelength option.
    """
    print("Choose a wavelength option:")
    print("1. 660nm")
    print("2. 810nm")
    print("3. 940nm")
    
    choice = int(input("Enter your choice (1-3): "))
    return choice

def retrieve_preset_value(choice):
    """
    Retrieve the preset value based on the user's choice.

    Parameters:
    int choice: The user's choice of wavelength option.

    Returns:
    float: The preset value corresponding to the choice.
    """
    preset_values = {
        1: (e_hbO2_660, e_hb_660),
        2: (e_hbO2_660, e_hb_810),
        3: (e_hbO2_940, e_hb_940)
    }
    return preset_values.get(choice, None)


def enter_measurements():
    """
    Function to enter measurements from the user.
 
    This function prompts the user to enter measurements for air, water, and blood.
    The measurements are entered in groups, with the first measurement being for air,
    the second measurement for water, and the third measurement for blood.
 
    Returns:
    tuple: A tuple containing the measurements for air, water, and blood in that order.
           Each measurement is a float value.
 
    Raises:
    - ValueError: If any of the entered measurements are not valid float values.
    """
 
    # Prompting the user to enter the measurements for air, water, and blood.
    air_red = float(input("The optical power measurement obtained from the red lED in air: "))
    water_red = float(input("The optical power measurement obtained from the red lED in water: "))
    blood_red = float(input("The optical power measurement obtained from the red lED in blood: "))
    air_nir = float(input("The optical power measurement obtained from the NIR lED in air: "))
    water_nir = float(input("The optical power measurement obtained from the NIR lED in water: "))
    blood_nir = float(input("The optical power measurement obtained from the NIR lED in blood: "))
 
    # Returning the measurements as a tuple.
    # return air_red, water_red, blood_red, air_nir, water_nir, blood_nir
    return

def calculate():
    """
    Function to calculate based on user input.
 
    This function asks the user to enter measurements in groups and performs calculations
    based on the entered measurements. It continues to ask for more measurements until the
    user chooses to stop.
 
    Returns:
    None
    """
 
    # Initializing a list to store the calculated results.
    results = []
 
    # Flag to control the loop for entering measurements.
    continue_entering = True
 
    while continue_entering:
        try:
            # Asking the user to enter measurements.
            measurements = enter_measurements()
 
            # Appending the measurements to the results list.
            results.append(measurements)
 
            # Asking the user if they want to enter more measurements.
            choice = input("Do you have another set of measurements to enter? (y/n): ")
 
            # Checking the user's choice to continue or stop entering measurements.
            if choice.lower() == 'n':
                continue_entering = False
 
        except ValueError:
            print("Invalid measurement entered. Please enter a valid float value.")
 

def calculate_with_preset_formula(value):
    """
    Perform a calculation using the preset formula.

    Parameters:
    float value: The preset value.

    Returns:
    float: The result of the calculation.
    """
    # Example formula: Multiply the value by 2
    result = value * 2
    return result

# Define all the necessary Extinction coefficients, Moaveni's data
# At 660nm, HbO2 has a ε of 320 [cm-1/M] and Hb has a ε of 3200 [cm-1/M];
# At 810nm, HbO2 has a ε of 860 [cm-1/M] and Hb has a ε of 880 [cm-1/M];
# At 940nm, HbO2 has a ε of 1200 [cm-1/M] and Hb has a ε of 800 [cm-1/M].
e_hbO2_660 = 320
e_hb_660 = 3200
e_hbO2_810 = 860
e_hb_810 = 880
e_hbO2_940 = 1200
e_hb_940 = 800



# Main code
choice = get_wavelength_option()

if 1 <= choice <= 3:
    value = retrieve_preset_value(choice)
    if value is not None:
        e_hbO2, e_hb = value
        print(f"Extinction coefficients of HbO2 and Hb: {e_hbO2},{e_hb}")
    else:
        print("Invalid choice. Preset value not found.")
else:
    print("Invalid choice. Please choose between 1 and 3.")


try:
    oxygen_saturation = calculate_oxygen_saturation(red_measurement, nir_measurement)
    print(f"The oxygen saturation is {oxygen_saturation}%.")
except ValueError as e:
    print(f"Error: {e}")
except ZeroDivisionError as e:
    print(f"Error: {e}")




# Unit tests for calculate_oxygen_saturation function.

import unittest

class TestCalculateOxygenSaturation(unittest.TestCase):

    def test_positive_power_measurements(self):
        """
        Tests the calculation of oxygen saturation with positive power measurements.
        """
        red_power = 10.0
        nir_power = 5.0
        expected_result = 0.5
        self.assertAlmostEqual(calculate_oxygen_saturation(red_power, nir_power), expected_result)

    def test_negative_power_measurements(self):
        """
        Tests if ValueError is raised when power measurements are negative.
        """
        red_power = -10.0
        nir_power = 5.0
        with self.assertRaises(ValueError):
            calculate_oxygen_saturation(red_power, nir_power)

        red_power = 10.0
        nir_power = -5.0
        with self.assertRaises(ValueError):
            calculate_oxygen_saturation(red_power, nir_power)

    def test_zero_red_power_measurement(self):
        """
        Tests the calculation of oxygen saturation when red power measurement is zero.
        """
        red_power = 0.0
        nir_power = 5.0
        expected_result = -1.0
        self.assertAlmostEqual(calculate_oxygen_saturation(red_power, nir_power), expected_result)

    def test_zero_nir_power_measurement(self):
        """
        Tests the calculation of oxygen saturation when NIR power measurement is zero.
        """
        red_power = 10.0
        nir_power = 0.0
        expected_result = 1.0
        self.assertAlmostEqual(calculate_oxygen_saturation(red_power, nir_power), expected_result)

    def test_zero_power_measurements(self):
        """
        Tests the calculation of oxygen saturation when both power measurements are zero.
        """
        red_power = 0.0
        nir_power = 0.0
        with self.assertRaises(ZeroDivisionError):
            calculate_oxygen_saturation(red_power, nir_power)

# Examples of using the calculate_oxygen_saturation function:

# Example 1: Calculating oxygen saturation with positive power measurements
red_power1 = 10.0
nir_power1 = 5.0
oxygen_saturation1 = calculate_oxygen_saturation(red_power1, nir_power1)
print(f"For red power measurement = {red_power1} and NIR power measurement = {nir_power1}, the oxygen saturation is {oxygen_saturation1}.")

# Example 2: Calculating oxygen saturation with negative power measurements (should raise an error)
try:
    red_power2 = -10.0
    nir_power2 = 5.0
    oxygen_saturation2 = calculate_oxygen_saturation(red_power2, nir_power2)
    print(f"For red power measurement = {red_power2} and NIR power measurement = {nir_power2}, the oxygen saturation is {oxygen_saturation2}.")
except ValueError as e:
    print(f"Error while calculating oxygen saturation: {e}")