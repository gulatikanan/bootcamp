"""
Short Circuiting with Any

Instructions:
Complete the exercise according to the requirements.
"""
big_list = range(1, 1000000)
has_divisible = any(x % 99 == 0 for x in big_list)
print("Found divisible by 99:", has_divisible)
