"""
Constants

Instructions:
Complete the exercise according to the requirements.
"""

def retry_operation():
    for i in range(3):  # Magic value '3'
        try:
            # Try some operation
            pass
        except:
            pass

MAX_RETRIES = 3  # Define the constant

def retry_operation():
    for i in range(MAX_RETRIES):  # Use the constant
        try:
            # Try some operation
            pass
        except:
            pass
