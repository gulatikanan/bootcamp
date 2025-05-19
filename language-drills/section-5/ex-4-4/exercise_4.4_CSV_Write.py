"""
CSV Write

Instructions:
Complete the exercise according to the requirements.
"""
import csv

# Data to write to CSV
data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "Los Angeles"}
]

# Write to CSV file
with open('output.csv', mode='w', newline='') as csvfile:
    fieldnames = ['name', 'age', 'city']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Write header
    writer.writerows(data)  # Write rows
