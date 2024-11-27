import random

def generate_fibonacci(n):
    """Generate a list of n Fibonacci numbers"""
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence


def sort_reverse_ascending(fib_sequence):
    """Sort the Fibonacci sequence in reverse ascending order"""
    sorted_fib = sorted(fib_sequence, reverse=True)
    return sorted_fib


# Generate a randomized Fibonacci sequence of length 10
fib_length = 10
randomized_fib = generate_fibonacci(fib_length)

# Sort the Fibonacci sequence in reverse ascending order
sorted_fib = sort_reverse_ascending(randomized_fib)

print("Randomized Fibonacci Sequence:", randomized_fib)
print("Sorted Fibonacci Sequence (reverse ascending):", sorted_fib)