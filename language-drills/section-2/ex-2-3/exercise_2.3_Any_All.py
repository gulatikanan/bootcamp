"""
Any All

Instructions:
Complete the exercise according to the requirements.
"""

nums = [1, -2, 3, 4]

# any(): check if any number is negative
print("Any negative?", any(n < 0 for n in nums))  # True

# all(): check if all numbers are positive
print("All positive?", all(n > 0 for n in nums))  # False
