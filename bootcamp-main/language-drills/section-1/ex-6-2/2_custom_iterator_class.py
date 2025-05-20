class Counter:
    def __init__(self, max):
        self.max = max
        self.cur = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.cur >= self.max:
            raise StopIteration
        self.cur += 1
        return self.cur
