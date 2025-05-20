"""
Use Islice

Instructions:
Complete the exercise according to the requirements.
"""

import itertools

# Slice the range from index 3 to 6
sliced = itertools.islice(range(10), 3, 7)
print(list(sliced))  # Outputs: [3, 4, 5, 6]
