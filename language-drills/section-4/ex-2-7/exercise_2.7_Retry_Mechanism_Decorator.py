"""
Retry Mechanism Decorator

Instructions:
Complete the exercise according to the requirements.
"""
import random

def retry(max_retries):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error occurred: {e}, retrying...")
            print("Max retries exceeded.")
        return wrapper
    return decorator

# Example usage
@retry(3)
def unstable_function():
    if random.random() < 0.5:
        raise ValueError("Something went wrong!")
    return "Success"

print(unstable_function())
