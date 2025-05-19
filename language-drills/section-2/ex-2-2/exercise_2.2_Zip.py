"""
Zip
"""

numbers = [1, 2, 3]
letters = ['a', 'b', 'c']

for num, letter in zip(numbers, letters):
    print(f"{num} paired with {letter}")
