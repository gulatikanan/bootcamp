"""
Safe Type Conversion EAFP


"""

value = "abc"

# Try converting to int and handle if it fails
try:
    num = int(value)
    print("Converted:", num)
except ValueError:
    print("Invalid number input (EAFP)")

