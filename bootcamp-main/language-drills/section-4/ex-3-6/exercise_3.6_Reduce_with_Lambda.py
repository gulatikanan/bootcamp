"""
Reduce with Lambda

Instructions:
Complete the exercise according to the requirements.
"""

from functools import reduce

# Compute factorial using reduce
factorial = reduce(lambda x, y: x * y, range(1, 6))  # 5! = 120
print(factorial)  # Output: 120
