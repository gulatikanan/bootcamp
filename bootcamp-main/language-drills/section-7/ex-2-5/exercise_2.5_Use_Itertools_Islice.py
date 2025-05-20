"""
Use Itertools Islice

Instructions:
Complete the exercise according to the requirements.
"""

from itertools import islice

def line_gen():
    with open("large.txt") as f:
        for line in f:
            yield line

for line in islice(line_gen(), 10):
    print(line.strip())
