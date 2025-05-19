"""
Manual Timing with Time

Instructions:
Complete the exercise according to the requirements.
"""

import time

start_time = time.time()
# Code to time
sum(range(10000))
end_time = time.time()

print(f"Execution time: {end_time - start_time} seconds")
