lst = [x for x in range(5) if x % 2 == 0]
gen = (x for x in range(5) if x % 2 == 0)
print(list(lst))  # [0, 2, 4]
print(list(gen))  # [0, 2, 4]

