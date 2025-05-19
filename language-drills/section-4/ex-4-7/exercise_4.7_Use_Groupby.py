"""
Use Groupby

Instructions:
Complete the exercise according to the requirements.
"""

import itertools

# Data to be grouped
data = [{'key': 'A', 'value': 1},
        {'key': 'B', 'value': 2},
        {'key': 'A', 'value': 3},
        {'key': 'B', 'value': 4},
        {'key': 'C', 'value': 5}]

# Sort data by key for groupby to work
data.sort(key=lambda x: x['key'])

# Group data by 'key'
grouped = itertools.groupby(data, key=lambda x: x['key'])

# Print the grouped data
for key, group in grouped:
    print(f"Group {key}: {list(group)}")
