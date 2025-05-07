"""
Composition of Decorators

Instructions:
Complete the exercise according to the requirements.
"""
# Re-using previous decorators
# Reusing previous decorators:
def simple_logger(func):
    def wrapper(*args, **kwargs):
        print("Function started")
        result = func(*args, **kwargs)
        print("Function ended")
        return result
    return wrapper

def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.6f} seconds")
        return result
    return wrapper

def debug_info(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Function: {func.__name__}")
        print(f"Arguments: {args}, {kwargs}")
        print(f"Return value: {result}")
        return result
    return wrapper

# Apply decorators
@simple_logger
@timer
@debug_info
def some_function(a, b):
    return a + b

# Example usage
some_function(2, 3)
