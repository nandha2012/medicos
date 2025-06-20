class Counter:
    def __init__(self):
        self.count = 0

    def inc(self):
        self.count += 1

    def value(self):
        return self.count
