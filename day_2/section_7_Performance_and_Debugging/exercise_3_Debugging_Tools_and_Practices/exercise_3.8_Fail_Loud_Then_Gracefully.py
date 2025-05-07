"""
Fail Loud Then Gracefully

Instructions:
Complete the exercise according to the requirements.
"""
def risky():
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print("Logging error:", e)
        raise  # Re-raise after logging

try:
    risky()
except ZeroDivisionError:
    print("Handled gracefully outside.")
