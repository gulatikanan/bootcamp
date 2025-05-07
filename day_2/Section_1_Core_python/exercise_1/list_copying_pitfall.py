a = [1, 2, 3]
b = a
c = a[:]  # proper copy
a[0] = 99

print(b)  # [99, 2, 3] – changed
print(c)  # [1, 2, 3] – unchanged
