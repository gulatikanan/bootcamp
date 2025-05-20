"""
Read a File with Pathlib

Instructions:
Complete the exercise according to the requirements.
"""

from pathlib import Path

# Read a file using pathlib
file_path = Path("myfile.txt")
content = file_path.read_text()

print(content)

