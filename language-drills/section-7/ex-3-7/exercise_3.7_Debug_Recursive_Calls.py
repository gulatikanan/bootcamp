"""
Debug Recursive Calls

Instructions:
Complete the exercise according to the requirements.
"""

def factorial(n, level=0):
    indent = " " * level
    print(f"{indent}factorial({n})")
    if n == 1:
        return 1
    return n * factorial(n - 1, level + 2)

print("Result:", factorial(4))
