from collections import deque

"""
append
popleft
size
empty
"""

class MyStack:

    def __init__(self):
        self.deque = deque()   
        self.helper = deque()
        
    def push(self, x: int) -> None:
        self.deque.append(x)

    def pop(self) -> int:
        while len(self.deque) > 1:
            self.helper.append(self.deque.popleft())
        result = self.deque.popleft()
        while len(self.helper) > 0:
            self.deque.append(self.helper.popleft())
        return result

    def top(self) -> int:
        while len(self.deque) > 1:
            self.helper.append(self.deque.popleft())
        result = self.deque.popleft()
        self.helper.append(result)
        while len(self.helper) > 0:
            self.deque.append(self.helper.popleft())
        return result

    def empty(self) -> bool:
        assert len(self.helper) == 0
        return len(self.deque) == 0

# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()
