"""
Measure Memory with Memory Profiler

Instructions:
Complete the exercise according to the requirements.
"""

from memory_profiler import profile

@profile
def memory_hog():
    a = [i for i in range(10000000)]
    return a

memory_hog()
