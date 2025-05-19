"""
Map and Filter

"""
nums = [1, 2, 3, 4, 5]

# map(): double each number
doubled = list(map(lambda x: x * 2, nums))
print("Doubled:", doubled)

# filter(): remove even numbers
odd_numbers = list(filter(lambda x: x % 2 != 0, nums))
print("Odds only:", odd_numbers)
