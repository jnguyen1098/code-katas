# TODO: redo this

class MovingAverage:

    def __init__(self, size: int):
        self.data = []
        self.size = size
        self.l = 0
        self.r = 0
        self.count = 0
        
    def next(self, val: int) -> float:
        self.data.append(val)
        self.count = min(self.size, self.count + 1)
        self.r += 1
        if self.r > self.size:
            self.l += 1
        return sum(self.data[self.l : self.r + 1]) / self.count
