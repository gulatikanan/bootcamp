"""
Function Metadata with Wraps

Instructions:
Complete the exercise according to the requirements.
"""

from functools import wraps

def preserve_metadata(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@preserve_metadata
def example_function():
    """This is a sample function."""
    return "Hello!"

# Test
print(example_function())  # Output: Hello!
print(example_function.__name__)  # Output: example_function
print(example_function.__doc__)  # Output: This is a sample function.
