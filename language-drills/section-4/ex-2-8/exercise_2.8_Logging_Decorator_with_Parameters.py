"""
Logging Decorator with Parameters

Instructions:
Complete the exercise according to the requirements.
"""

def custom_logger(log_message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"LOG: {log_message} - Before execution")
            result = func(*args, **kwargs)
            print(f"LOG: {log_message} - After execution")
            return result
        return wrapper
    return decorator

# Example usage
@custom_logger("Function call")
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
