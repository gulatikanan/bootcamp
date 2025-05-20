"""
Check Exit Code

Instructions:
Complete the exercise according to the requirements.
"""
import subprocess

# Run a command and check the exit code
result = subprocess.run(["ls", "-l"])  # On Windows, use ["dir"]
print("Exit Code:", result.returncode)

# Check if the subprocess failed (non-zero exit code indicates failure)
if result.returncode != 0:
    print("Command failed")
else:
    print("Command succeeded")
