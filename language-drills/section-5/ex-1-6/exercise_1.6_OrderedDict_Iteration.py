"""
OrderedDict Iteration

Instructions:
Complete the exercise according to the requirements.
"""

import collections

# Create an OrderedDict
ordered_dict = collections.OrderedDict()
ordered_dict['apple'] = 1
ordered_dict['banana'] = 2
ordered_dict['cherry'] = 3

# Iterate over the ordered dictionary
for key, value in ordered_dict.items():
    print(key, value)
# Outputs:
# apple 1
# banana 2
# cherry 3
