"""
Large Data with Generators

Instructions:
Complete the exercise according to the requirements.
"""

def read_large_file(file_path):
    with open(file_path, "r") as f:
        for line in f:
            yield line

# Example usage
for line in read_large_file("large.txt"):
    print(line.strip())
