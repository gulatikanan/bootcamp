"""
When to Prefer LBYL


"""

def square(x):
    if isinstance(x, (int, float)):
        return x * x
    else:
        return "Not a number"

print(square(5))      # 25
print(square("hi"))   # Not a number
