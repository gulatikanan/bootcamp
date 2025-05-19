"""
Debug Information Decorator

Instructions:
Complete the exercise according to the requirements.
"""
def debug_info(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Function: {func.__name__}")
        print(f"Arguments: {args}, {kwargs}")
        print(f"Return value: {result}")
        return result
    return wrapper

# Example usage
@debug_info
def multiply(a, b):
    return a * b

multiply(2, 3)
