"""
Nested Defaultdict

Instructions:
Complete the exercise according to the requirements.
"""
import collections

# Create a defaultdict of defaultdicts
nested_dd = collections.defaultdict(lambda: collections.defaultdict(int))

# Set values in the nested dictionary
nested_dd['a']['x'] = 10
nested_dd['b']['y'] = 20

print(nested_dd)
# Outputs: defaultdict(<function <lambda> at 0x7f4c8e5561f0>, {'a': defaultdict(<class 'int'>, {'x': 10}), 'b': defaultdict(<class 'int'>, {'y': 20})})
