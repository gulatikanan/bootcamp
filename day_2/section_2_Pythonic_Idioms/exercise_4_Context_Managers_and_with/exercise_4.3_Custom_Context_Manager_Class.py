"""
Custom Context Manager Class

Instructions:
Complete the exercise according to the requirements.
"""

class MyContext:
    def __enter__(self):
        print("Entering context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting context")

with MyContext():
    print("Inside context")

