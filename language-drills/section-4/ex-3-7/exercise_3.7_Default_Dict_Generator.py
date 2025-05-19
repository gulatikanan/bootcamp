"""
Default Dict Generator

Instructions:
Complete the exercise according to the requirements.
"""

from functools import partial

# Create a partial function to generate nested dicts
default_dict = partial(dict, **{"nested": {"inner_key": "value"}})

# Test
nested_dict = default_dict()
print(nested_dict)  # Output: {'nested': {'inner_key': 'value'}}
