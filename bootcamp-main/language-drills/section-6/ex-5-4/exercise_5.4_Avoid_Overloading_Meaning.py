"""
Avoid Overloading Meaning

Instructions:
Complete the exercise according to the requirements.
"""

def process_temp(data):  # 'temp' and 'data' are ambiguous
    result = [x * 2 for x in data]
    return result

def process_numbers(numbers):  # 'numbers' is specific
    result = [x * 2 for x in numbers]
    return result
