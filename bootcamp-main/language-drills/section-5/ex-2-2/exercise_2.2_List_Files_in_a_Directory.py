"""
List Files in a Directory

Instructions:
Complete the exercise according to the requirements.
"""

from pathlib import Path

# List all Python files in the current directory
for py_file in Path(".").glob("*.py"):
    print(py_file)
