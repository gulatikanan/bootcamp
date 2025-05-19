"""
Generator vs List Memory

Instructions:
Complete the exercise according to the requirements.
"""

import sys

gen_expr = (x for x in range(1000000))
list_obj = [x for x in range(1000000)]

print("Generator size:", sys.getsizeof(gen_expr))  # small
print("List size:", sys.getsizeof(list_obj))       # large
