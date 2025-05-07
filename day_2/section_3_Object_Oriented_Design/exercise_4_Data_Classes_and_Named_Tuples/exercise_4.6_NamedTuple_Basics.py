"""
NamedTuple Basics

Instructions:
Complete the exercise according to the requirements.
"""

from collections import namedtuple

# Define the namedtuple with fields 'x' and 'y'
Point = namedtuple('Point', ['x', 'y'])

# Create a Point instance
p = Point(1, 2)

# Access the fields
print(p.x)  # Output: 1
print(p.y)  # Output: 2
