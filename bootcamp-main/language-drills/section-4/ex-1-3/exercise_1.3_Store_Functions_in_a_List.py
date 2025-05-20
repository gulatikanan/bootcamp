"""
Store Functions in a List

Instructions:
Complete the exercise according to the requirements.
"""

funcs = [abs, str, hex]

# Apply each function to -42
results = [func(-42) for func in funcs]
print(results)  # Output: [42, '-42', '-0x2a']
