matrix = [[1, 2], [3, 4]]
flat = [item for sub in matrix for item in sub]
print(flat)  # [1, 2, 3, 4]
