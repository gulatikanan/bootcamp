# Generator Expression: Use (n*n for n in range(5)) to build a generator and print its items.

gen = (n*n for n in range(5))
for val in gen:
    print(val, end=" ")  # 0 1 4 9 16
