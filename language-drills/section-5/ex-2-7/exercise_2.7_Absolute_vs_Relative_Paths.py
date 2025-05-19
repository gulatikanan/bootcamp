"""
Absolute vs Relative Paths

Instructions:
Complete the exercise according to the requirements.
"""

from pathlib import Path

# Show the absolute path of a file
relative_path = Path("myfile.txt")
absolute_path = relative_path.resolve()

print(f"Absolute path: {absolute_path}")
