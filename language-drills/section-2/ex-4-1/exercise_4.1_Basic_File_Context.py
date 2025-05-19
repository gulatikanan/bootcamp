"""
Basic File Context

Instructions:
Complete the exercise according to the requirements.
"""

# Make sure 'sample.txt' exists
with open('sample.txt', 'r') as f:
    contents = f.read()
    print("File contents:", contents)
