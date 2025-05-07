"""
Multiple Contexts

Instructions:
Complete the exercise according to the requirements.
"""

with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    data = infile.read()
    outfile.write(data)
    print("Copied contents from input.txt to output.txt")
