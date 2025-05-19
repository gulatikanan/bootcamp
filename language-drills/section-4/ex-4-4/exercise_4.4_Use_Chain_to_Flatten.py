"""
Use Chain to Flatten

Instructions:
Complete the exercise according to the requirements.
"""

import itertools

# Combine lists into one iterator
combined = itertools.chain([1, 2], [3, 4], [5])
print(list(combined))  # Outputs: [1, 2, 3, 4, 5]
