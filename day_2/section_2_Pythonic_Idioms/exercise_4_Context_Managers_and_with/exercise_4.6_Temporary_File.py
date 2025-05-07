"""
Temporary File

Instructions:
Complete the exercise according to the requirements.
"""

import tempfile

with tempfile.TemporaryFile(mode='w+t') as tmp:
    tmp.write("Hello, temporary file!")
    tmp.seek(0)
    print(tmp.read())
