"""
Capture Output

Instructions:
Complete the exercise according to the requirements.
"""

import subprocess

# Run a command and capture its output
result = subprocess.run(["echo", "Hello, World!"], capture_output=True, text=True)
print("Captured Output:", result.stdout)  # stdout contains the command's output
