from statistics import median

def calculate_average_median(*values):
    """
    Calculates the average and median of a given set of values.

    This function takes multiple values as input and calculates their average
    and median. The average is calculated by summing all the values and dividing
    by the total count. The median is the middle value of the sorted list of values.

    Parameters:
    - *values: Variable number of input values.

    Returns:
    tuple: A tuple containing the average and median of the input values.

    Raises:
    - ValueError: If no values are provided.

    Examples:
    >>> calculate_average_median(1, 2, 3, 4, 5)
    (3.0, 3)
    >>> calculate_average_median(10, 20, 30, 40, 50, 60)
    (35.0, 35)
    >>> calculate_average_median(2)
    (2.0, 2)
    """

    # Checking if any values are provided
    if len(values) == 0:
        raise ValueError("No values provided.")

    # Calculating the average
    average = sum(values) / len(values)

    # Calculating the median
    median_value = median(values)

    # Returning the average and median as a tuple
    return average, median_value

# Example usage of the calculate_average_median function

# Example 1: Calculating average and median of multiple values
values1 = [1, 2, 3, 4, 5]
average1, median1 = calculate_average_median(*values1)
print(f"For the values {values1}, the average is {average1} and the median is {median1}.")

# Example 2: Calculating average and median of a single value
values2 = [10]
average2, median2 = calculate_average_median(*values2)
print(f"For the value {values2}, the average is {average2} and the median is {median2}.")

# Example 3: Calculating average and median of no values (should raise an error)
try:
    average3, median3 = calculate_average_median()
    print(f"For no values, the average is {average3} and the median is {median3}.")
except ValueError as e:
    print(f"Error: {e}")