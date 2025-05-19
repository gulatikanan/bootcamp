try:
    x = int("abc") / 0
except ValueError:
    print("Value Error")
except ZeroDivisionError:
    print("Zero Division")
