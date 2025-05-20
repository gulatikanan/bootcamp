"""
Partial Function

Instructions:
Complete the exercise according to the requirements.
"""

from functools import partial

# Partial function to convert a string to a base 2 integer
base2_int = partial(int, base=2)

# Test
print(base2_int('1010'))  # Output: 10 (binary 1010 -> decimal 10)
