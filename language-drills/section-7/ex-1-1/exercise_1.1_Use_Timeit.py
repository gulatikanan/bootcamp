"""
Use Timeit

Instructions:
Complete the exercise according to the requirements.
"""

import timeit

# Timing the sum operation
execution_time = timeit.timeit("sum(range(10000))", number=100)
print(f"Execution time: {execution_time} seconds")

