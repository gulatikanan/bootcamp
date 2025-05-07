"""
Pretty Print JSON

Instructions:
Complete the exercise according to the requirements.
"""
import json

# Python dict
data = {"name": "Alice", "age": 30, "city": "New York"}

# Pretty print JSON with sorted keys
pretty_json = json.dumps(data, indent=4, sort_keys=True)
print("Pretty Printed JSON:\n", pretty_json)
