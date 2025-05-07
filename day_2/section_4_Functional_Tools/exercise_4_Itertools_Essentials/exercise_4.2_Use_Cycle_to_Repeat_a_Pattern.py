"""
Use Cycle to Repeat a Pattern

Instructions:
Complete the exercise according to the requirements.
"""

import itertools

# Cycle through colors
pattern = itertools.cycle(["red", "green", "blue"])

# Print 6 items from the cycle
for _ in range(6):
    print(next(pattern), end=" ")  # Outputs: red green blue red green blue
