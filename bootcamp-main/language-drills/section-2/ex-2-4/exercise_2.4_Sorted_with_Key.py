"""
Sorted with Key

"""

pairs = [(1, 3), (2, 2), (4, 1)]

# Sort based on second item of each tuple
sorted_pairs = sorted(pairs, key=lambda x: x[1])
print("Sorted by second item:", sorted_pairs)
