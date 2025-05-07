"""
CSV Read

Instructions:
Complete the exercise according to the requirements.
"""
import csv

# Assuming data.csv contains:
# name,age,city
# Alice,30,New York
# Bob,25,Los Angeles

with open('data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
