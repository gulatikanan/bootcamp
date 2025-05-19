# Conditional Assignment in Comprehension: Replace negative numbers with 0 in a list using a comprehension.

nums = [-2, 3, -1, 4]
print([x if x >= 0 else 0 for x in nums])  # [0, 3, 0, 4]
