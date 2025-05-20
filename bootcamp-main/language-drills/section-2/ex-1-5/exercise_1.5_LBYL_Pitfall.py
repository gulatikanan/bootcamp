import os

filename = "testfile.txt"

# LBYL (not safe in multi-threaded or real-world FS environments)
if os.path.exists(filename):
    with open(filename, "r") as f:
        print(f.read())
# If another program deletes the file after the check but before open(), it crashes
