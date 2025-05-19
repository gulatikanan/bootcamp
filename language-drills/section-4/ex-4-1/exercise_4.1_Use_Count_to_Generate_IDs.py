"""
Use Count to Generate IDs

Instructions:
Complete the exercise according to the requirements.
"""

import itertools

id_gen = itertools.count(start=1)
for _ in range(5):
    print(next(id_gen), end=" ")  # Outputs: 1 2 3 4 5
