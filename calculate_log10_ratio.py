import math

def calculate_log10_ratio(x: float, y: float) -> float:
    """
    Calculates the logarithm base 10 of the ratio between two numbers.

    This function takes two numbers, x and y, and computes the logarithm base 10
    of their ratio (x / y).

    Parameters:
    - x (float): The numerator of the ratio.
    - y (float): The denominator of the ratio.

    Returns:
    float: The logarithm base 10 of the ratio (x / y).

    Raises:
    - ValueError: If the denominator (y) is zero, which would result in a division by zero.

    Examples:
    >>> calculate_log10_ratio(10, 2)
    0.6989700043360189

    >>> calculate_log10_ratio(100, 10)
    1.0

    >>> calculate_log10_ratio(1, 0)
    Traceback (most recent call last):
        ...
    ValueError: Denominator (y) should not be zero.
    """

    # Checking if the denominator (y) is zero
    if y == 0:
        raise ValueError("Denominator (y) should not be zero.")

    # Calculating the logarithm base 10 of the ratio (x / y)
    result = math.log10(x / y)

    # Returning the calculated result
    return result

# Example usage:
x_value = 10
y_value = 2
log_ratio = calculate_log10_ratio(x_value, y_value)
print(f"The logarithm base 10 of {x_value} / {y_value} is {log_ratio}.")