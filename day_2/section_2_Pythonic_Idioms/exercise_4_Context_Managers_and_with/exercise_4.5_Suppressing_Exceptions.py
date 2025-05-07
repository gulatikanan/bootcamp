"""
Suppressing Exceptions

Instructions:
Complete the exercise according to the requirements.
"""

from contextlib import suppress

with suppress(FileNotFoundError):
    with open('nonexistent.txt', 'r') as f:
        print(f.read())
print("Program continues without crashing.")

