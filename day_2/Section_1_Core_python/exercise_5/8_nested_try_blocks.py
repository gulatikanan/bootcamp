try:
    try:
        x = int("abc")
    except ValueError:
        print("Inner error")
except Exception:
    print("Outer error")
