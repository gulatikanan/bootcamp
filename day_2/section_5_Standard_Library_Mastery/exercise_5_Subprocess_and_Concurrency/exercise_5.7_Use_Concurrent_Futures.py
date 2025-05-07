"""
Use Concurrent Futures

Instructions:
Complete the exercise according to the requirements.
"""

import concurrent.futures

# Function to compute square
def compute_square(number):
    return number * number

# Use ThreadPoolExecutor to execute functions concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    numbers = [1, 2, 3, 4, 5]
    results = list(executor.map(compute_square, numbers))

print("Squares:", results)
