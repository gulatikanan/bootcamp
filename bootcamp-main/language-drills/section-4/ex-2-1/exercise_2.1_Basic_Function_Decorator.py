"""
Basic Function Decorator

Instructions:
Complete the exercise according to the requirements.
"""

def simple_logger(func):
    def wrapper(*args, **kwargs):
        print("Function started")
        result = func(*args, **kwargs)
        print("Function ended")
        return result
    return wrapper

# Example usage
@simple_logger
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
