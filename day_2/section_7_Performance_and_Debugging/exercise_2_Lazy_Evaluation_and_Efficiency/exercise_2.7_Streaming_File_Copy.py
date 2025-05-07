"""
Streaming File Copy

Instructions:
Complete the exercise according to the requirements.
"""
with open("source.txt", "r") as src, open("dest.txt", "w") as dst:
    for line in src:
        dst.write(line)
