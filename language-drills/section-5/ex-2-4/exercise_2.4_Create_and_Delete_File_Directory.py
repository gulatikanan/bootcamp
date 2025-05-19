"""
Create and Delete File Directory

Instructions:
Complete the exercise according to the requirements.
"""

import os
import shutil
from pathlib import Path

# Create a directory
os.makedirs("temp_directory", exist_ok=True)

# Delete a directory (and its contents)
shutil.rmtree("temp_directory")
