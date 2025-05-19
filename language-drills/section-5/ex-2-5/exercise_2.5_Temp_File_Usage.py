"""
Temp File Usage

Instructions:
Complete the exercise according to the requirements.
"""
import tempfile

# Create a temporary file and write to it
with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    temp_file.write(b"Temporary file content")
    print(f"Temporary file created: {temp_file.name}")
