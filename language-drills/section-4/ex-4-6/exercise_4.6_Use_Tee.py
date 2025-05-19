"""
Use Tee

Instructions:
Complete the exercise according to the requirements.
"""

import itertools

# Create an iterator from a list
original = iter([10, 20, 30, 40])

# Duplicate the iterator
iter1, iter2 = itertools.tee(original, 2)

# Print both iterators independently
print("Iterator 1:", list(iter1))  # Outputs: [10, 20, 30, 40]
print("Iterator 2:", list(iter2))  # Outputs: [10, 20, 30, 40]
