t = (1, 2, 3)
try:
    t[0] = 99
except TypeError as e:
    print(e)  # 'tuple' object does not support item assignment
