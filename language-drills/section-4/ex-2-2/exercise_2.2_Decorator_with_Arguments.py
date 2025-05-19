"""
Decorator with Arguments

Instructions:
Complete the exercise according to the requirements.
"""

def prefix_printer(prefix):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"{prefix} - Calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Example usage
@prefix_printer("INFO")
def add(a, b):
    return a + b

add(2, 3)
