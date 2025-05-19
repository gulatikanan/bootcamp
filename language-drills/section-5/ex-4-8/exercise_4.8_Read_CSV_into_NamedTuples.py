"""
Read CSV into NamedTuples

Instructions:
Complete the exercise according to the requirements.
"""

import csv
from collections import namedtuple

# Define a namedtuple to store CSV rows
Person = namedtuple('Person', ['name', 'age', 'city'])

# Read from CSV and store rows in NamedTuples
with open('data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Skip the header
    for row in reader:
        person = Person(*row)
        print(person)
