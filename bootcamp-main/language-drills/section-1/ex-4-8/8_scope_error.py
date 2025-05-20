def bad():
    print(x)  # UnboundLocalError
    x = 5
try:
    bad()
except Exception as e:
    print(e)
