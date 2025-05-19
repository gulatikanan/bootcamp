def echo():
    while True:
        val = yield
        print(val)

gen = echo()
next(gen)
gen.send("Hello")
