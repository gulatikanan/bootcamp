"""
Start a Process

Instructions:
Complete the exercise according to the requirements.
"""

import multiprocessing

# Function to run in a separate process
def compute_square(number):
    print(f"Square of {number}: {number * number}")

# Create and start a process
process = multiprocessing.Process(target=compute_square, args=(5,))
process.start()

# Wait for the process to finish
process.join()
