"""
Use Permutations and Combinations

Instructions:
Complete the exercise according to the requirements.
"""

import itertools

# Generate all permutations (pairs) of [1, 2, 3]
perm = itertools.permutations([1, 2, 3], 2)
print("Permutations (pairs):", list(perm))  
# Outputs: [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# Generate all combinations (triples) of [1, 2, 3]
comb = itertools.combinations([1, 2, 3], 3)
print("Combinations (triples):", list(comb))  
# Outputs: [(1, 2, 3)]
