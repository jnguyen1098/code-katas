class MyCalendar:

    def __init__(self):
        self.intervals = set()

    def book(self, start: int, end: int) -> bool:
        for x, y in self.intervals:
            if end > x and start < y:
                return False
        self.intervals.add((start, end))
        return True
