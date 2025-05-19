try:
    raise ValueError("Oops")
except ValueError as e:
    print("Logging:", e)
    raise
