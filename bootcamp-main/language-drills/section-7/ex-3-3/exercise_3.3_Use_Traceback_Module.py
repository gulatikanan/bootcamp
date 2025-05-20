"""
Use Traceback Module

Instructions:
Complete the exercise according to the requirements.
"""
import traceback

try:
    1 / 0
except ZeroDivisionError:
    print("Error occurred:")
    print(traceback.format_exc())
