"""
Use Pdb Set Trace

Instructions:
Complete the exercise according to the requirements.
"""

import pdb

def debug_example():
    x = 10
    y = 5
    pdb.set_trace()  # Execution pauses here
    result = x + y
    print("Result:", result)

debug_example()
