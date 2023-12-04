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

def get_wavelength_option():
    """
    Prompt the user to choose a wavelength option.
    Returns:
    int: The user's choice of wavelength option.
    """
    print("Choose a wavelength:")
    print("1. 660nm")
    print("2. 810nm")
    print("3. 940nm")
    
    choice = int(input("Enter your choice of wavelength for entering measurements (1-3): "))
    return choice


def enter_measurements(choice):
    """
    Function to enter measurements from the user.
    This function prompts the user to enter measurements for air and sample.
    Returns:
    tuple: A tuple containing the measurements for air and sample in that order.
           Each measurement is a float value.
    """
    if choice == 1:
        air = float(input("The optical power measurement obtained from the red LED in air: "))
        sample = float(input("The optical power measurement obtained from the red LED in sample: "))
    elif choice == 2 or choice == 3:
        air = float(input("The optical power measurement obtained from the NIR LED in air: "))
        sample = float(input("The optical power measurement obtained from the NIR LED in sample: "))
    return air, sample

def calculate():
    """
    Calculate ScvO2 based on measurements and choice of wavelength.
    Parameters:
    int choice: The user's choice of wavelength option.
    float air: Measurement in air.
    float sample: Measurement in sample.
    """
    # Initialize lists to store the measurements.
    A_red_list = []
    A_Nir_list = []
    
    # Flag to control the loop for entering measurements.
    continue_entering = True

    red_entered = False
    nir_entered = False

    while continue_entering:
        try:
            choice = get_wavelength_option()

            air, sample = enter_measurements(choice)

            if choice == 1:
                A_red = math.log10(air / sample)
                A_red_list.append(A_red)
                red_entered = True
            elif choice == 2 or choice == 3:
                A_Nir = math.log10(air / sample)
                A_Nir_list.append(A_Nir)
                nir_entered = True


            option = input("Do you have another set of measurements to enter? (y/n): ")

            if option.lower() == 'n'and (red_entered and nir_entered):
                continue_entering = False

        except ValueError:
            print("Invalid measurement entered. Please enter a valid float value.")
    
    if not (red_entered and nir_entered):
        raise ValueError("At least one set of data in red and one in NIR is required.")

    R = A_red / A_Nir
    e_hb_red = e_hb_660
    e_hbO2_red = e_hbO2_660
    
    if choice == 2:
        e_hb_Nir = e_hb_810
        e_hbO2_Nir = e_hbO2_810
    elif choice == 3:
        e_hb_Nir = e_hb_940
        e_hbO2_Nir = e_hbO2_940
    
    ScvO2 = (e_hb_red - R * e_hb_Nir) / (e_hb_red - e_hbO2_red + R * (e_hbO2_Nir - e_hb_Nir)) * 100 

    print(f"Calculated results: {round(ScvO2, 2)}%")

# Main execution starts here

calculate()
