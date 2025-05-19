"""
Field Rename

Instructions:
Complete the exercise according to the requirements.
"""

from collections import namedtuple

# Define the namedtuple with valid field names
Point = namedtuple('Point', ['x', 'y', 'z'])

# This will create a Point instance
p = Point(1, 2, 3)

# Access the fields
print(p.x)  # Output: 1
print(p.y)  # Output: 2
print(p.z)  # Output: 3

# Invalid field names, starting with numbers or containing spaces
try:
    InvalidPoint = namedtuple('InvalidPoint', ['123x', 'y value'])
except ValueError as e:
    print(f"Error: {e}")

