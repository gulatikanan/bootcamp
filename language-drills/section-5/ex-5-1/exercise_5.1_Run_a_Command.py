"""
Run a Command

Instructions:
Complete the exercise according to the requirements.
"""

import subprocess

# Run a command to list files in the current directory
subprocess.run(["ls", "-l"])  # On Windows, use ["dir"]
