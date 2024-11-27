import random

def generate_fibonacci(n):
    """Generate first n Fibonacci numbers"""
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

def sort_fibonacci(fib_sequence):
    """Sort a randomized sequence of Fibonacci numbers"""
    # Randomize the sequence
    random.shuffle(fib_sequence)
    
    # Sort the sequence using Python's built-in sorted function
    sorted_fib_sequence = sorted(fib_sequence)
    
    return sorted_fib_sequence

# Generate 10 Fibonacci numbers and sort them
fib_numbers = generate_fibonacci(10)
print("Randomized Fibonacci sequence:", fib_numbers)

sorted_fib_numbers = sort_fibonacci(fib_numbers)
print("Sorted Fibonacci sequence:", sorted_fib_numbers)