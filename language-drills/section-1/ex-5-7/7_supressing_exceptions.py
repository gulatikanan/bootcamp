from contextlib import suppress
d = {}
with suppress(KeyError):
    print(d["missing"])
