"""
Timing Decorator

Instructions:
Complete the exercise according to the requirements.
"""

import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.6f} seconds")
        return result
    return wrapper

# Example usage
@timer
def long_running_function():
    time.sleep(2)

long_running_function()
