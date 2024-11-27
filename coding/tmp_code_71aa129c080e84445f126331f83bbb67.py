def sum_numbers(num1, num2):
    """
    This function takes two numbers as input and returns their sum.
    
    Parameters:
    num1 (int): The first number
    num2 (int): The second number
    
    Returns:
    int: The sum of the two numbers
    """
    return num1 + num2

# Test the function with 86 and 77
try:
    result = sum_numbers(86, 77)
    print("The sum is:", result)
except Exception as e:
    print(f"An error occurred: {e}")