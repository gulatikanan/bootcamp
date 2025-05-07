# EAFP: Try opening file, handle if not found
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("File not found (EAFP)")
