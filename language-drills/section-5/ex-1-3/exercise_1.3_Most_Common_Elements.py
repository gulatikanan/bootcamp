"""
Most Common Elements

Instructions:
Complete the exercise according to the requirements.
"""

import collections

# List of numbers
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5]

# Use most_common to get the top 2 most common elements
counter = collections.Counter(numbers)
print(counter.most_common(2))
# Outputs: [(4, 4), (3, 3)]  # (element, count)
