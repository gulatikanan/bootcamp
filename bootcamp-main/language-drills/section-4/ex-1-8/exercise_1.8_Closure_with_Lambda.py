"""
Closure with Lambda

Instructions:
Complete the exercise according to the requirements.
"""

def make_multiplier(factor):
    return lambda x: x * factor

# Example usage
multiplier_3 = make_multiplier(3)
print(multiplier_3(5))  # Output: 15
