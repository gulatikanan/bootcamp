"""
Defaultdict with Lambda

Instructions:
Complete the exercise according to the requirements.
"""

import collections

# Create a defaultdict with lambda to return "N/A" for missing keys
dd = collections.defaultdict(lambda: "N/A")
print(dd['apple'])  # Outputs: N/A
dd['apple'] = 1
print(dd['apple'])  # Outputs: 1
