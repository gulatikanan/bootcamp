"""
Write to a File

Instructions:
Complete the exercise according to the requirements.
"""

from pathlib import Path

# Write "hello" to a file
file_path = Path("myfile.txt")
file_path.write_text("hello")
