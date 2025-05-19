"""
Avoid Nesting

Instructions:
Complete the exercise according to the requirements.
"""

def check_conditions(x, y):
    if x > 10:
        if y < 5:
            return True
    return False

def is_greater_than_10(x):
    return x > 10

def is_less_than_5(y):
    return y < 5

def check_conditions(x, y):
    if is_greater_than_10(x) and is_less_than_5(y):
        return True
    return False
