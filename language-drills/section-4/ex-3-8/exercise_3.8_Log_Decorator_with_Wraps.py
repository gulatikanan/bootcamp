"""
Log Decorator with Wraps

Instructions:
Complete the exercise according to the requirements.
"""
from functools import wraps

def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Before executing {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After executing {func.__name__}")
        return result
    return wrapper

@log_decorator
def sample_function(a, b):
    return a + b

# Test
print(sample_function(2, 3))  # Output: Before executing sample_function
                             #          After executing sample_function
                             #          5
