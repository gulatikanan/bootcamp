"""
Use Warnings Module

Instructions:
Complete the exercise according to the requirements.
"""
import warnings

def old_function():
    warnings.warn("This function is deprecated", category=DeprecationWarning)
    return 42

old_function()
