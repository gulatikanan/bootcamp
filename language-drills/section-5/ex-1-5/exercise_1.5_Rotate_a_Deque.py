"""
Rotate a Deque

Instructions:
Complete the exercise according to the requirements.
"""

import collections

# Create a deque and rotate by 2 positions
dq = collections.deque([1, 2, 3, 4, 5])
dq.rotate(2)

print(dq)  # Outputs: deque([4, 5, 1, 2, 3])
