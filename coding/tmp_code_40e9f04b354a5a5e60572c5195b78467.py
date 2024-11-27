import random

# Function to generate Fibonacci numbers
def generate_fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

# Function to sort Fibonacci numbers in ascending order
def sort_fibonacci(numbers):
    return sorted(numbers)

# Generate a list of random Fibonacci numbers
fib_list = generate_fibonacci(10)
print("Random Fibonacci List:", fib_list)

# Sort the Fibonacci numbers in ascending order
sorted_fib_list = sort_fibonacci(fib_list)
print("Sorted Fibonacci List:", sorted_fib_list)