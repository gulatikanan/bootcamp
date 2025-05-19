"""
Lazy CSV Filter

Instructions:
Complete the exercise according to the requirements.
"""

import csv

def filtered_rows(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["age"]) > 30:
                yield row

# Example:
for row in filtered_rows("people.csv"):
    print(row)
