"""
Verbose Exceptions

Instructions:
Complete the exercise according to the requirements.
"""
try:
    int("abc")
except Exception as e:
    print("Caught exception:", type(e).__name__, "-", e)
