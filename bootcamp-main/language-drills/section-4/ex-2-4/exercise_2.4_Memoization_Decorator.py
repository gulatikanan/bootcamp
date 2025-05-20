"""
Memoization Decorator

Instructions:
Complete the exercise according to the requirements.
"""

import time
from functools import wraps

def memoize(func):
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            print("Returning cached result")
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

# Example usage
@memoize
def slow_function(x):
    print("Function is running...")
    time.sleep(1)  # Simulate a long-running function
    return x * 2

# First call, will take time and cache the result
print(slow_function(3))  

# Second call, should return the cached result
print(slow_function(3))  
