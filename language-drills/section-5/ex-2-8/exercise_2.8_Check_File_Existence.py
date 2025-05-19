"""
Check File Existence

Instructions:
Complete the exercise according to the requirements.
"""

from pathlib import Path

# Check if file exists and is a file
file_path = Path("myfile.txt")

if file_path.exists():
    print("File exists.")
    if file_path.is_file():
        print("It's a file.")
    else:
        print("It's a directory.")
else:
    print("File does not exist.")
