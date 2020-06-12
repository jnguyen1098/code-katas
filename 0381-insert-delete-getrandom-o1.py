class RandomizedSet:

    def __init__(self):
        self.set = set()
        

    def insert(self, val: int) -> bool:
        if val in self.set:
            return False
        self.set.add(val)
        return True
        

    def remove(self, val: int) -> bool:
        if val not in self.set:
            return False
        self.set.remove(val)
        return True
        

    def getRandom(self) -> int:
        return random.choice(tuple(self.set))
