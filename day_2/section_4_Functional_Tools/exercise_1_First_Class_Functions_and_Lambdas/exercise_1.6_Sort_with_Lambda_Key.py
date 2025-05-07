"""
Sort with Lambda Key

Instructions:
Complete the exercise according to the requirements.
"""

pairs = [(1, "b"), (2, "a")]
sorted_pairs = sorted(pairs, key=lambda x: x[1])  # Sort by the second element (the string)
print(sorted_pairs)  # Output: [(2, 'a'), (1, 'b')]
