len = 5
try:
    print(len(["a"]))  # TypeError
except TypeError as e:
    print("Error:", e)
