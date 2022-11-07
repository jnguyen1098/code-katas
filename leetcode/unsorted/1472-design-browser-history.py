class Node:
    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

class BrowserHistory:

    def __init__(self, homepage: str):
        self.curr_page = Node(data=homepage)
        self.index = 0

    def visit(self, url: str) -> None:
        new_page = Node(data=url, prev=self.curr_page, next=None)
        self.curr_page.next = new_page
        self.curr_page = new_page
        self.index += 1

    def back(self, steps: int) -> str:
        for _ in range(steps):
            if self.curr_page.prev is None:
                break
            self.index -= 1
            self.curr_page = self.curr_page.prev
        return self.curr_page.data

    def forward(self, steps: int) -> str:
        for _ in range(steps):
            if self.curr_page.next is None:
                break
            self.index += 1
            self.curr_page = self.curr_page.next
        return self.curr_page.data


# Your BrowserHistory object will be instantiated and called as such:
# obj = BrowserHistory(homepage)
# obj.visit(url)
# param_2 = obj.back(steps)
# param_3 = obj.forward(steps)class Node:
    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

class BrowserHistory:

    def __init__(self, homepage: str):
        self.curr_page = Node(data=homepage)
        self.index = 0

    def visit(self, url: str) -> None:
        new_page = Node(data=url, prev=self.curr_page, next=None)
        self.curr_page.next = new_page
        self.curr_page = new_page
        self.index += 1

    def back(self, steps: int) -> str:
        for _ in range(steps):
            if self.curr_page.prev is None:
                break
            self.index -= 1
            self.curr_page = self.curr_page.prev
        return self.curr_page.data

    def forward(self, steps: int) -> str:
        for _ in range(steps):
            if self.curr_page.next is None:
                break
            self.index += 1
            self.curr_page = self.curr_page.next
        return self.curr_page.data
