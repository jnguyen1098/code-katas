#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

class Board:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def right(self, col, incr=1):
        return (col + incr) % self.cols

    def down(self, row, incr=1):
        return (row + incr) % self.rows

    def advance(self):
        changed = 0
        # Advance east
        reqs = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == ">" and self.data[i][self.right(j)] == ".":
                    reqs.append((i, j))
        changed += len(reqs)
        while reqs:
            nx, ny = reqs.pop()
            self.data[nx][ny] = "."
            self.data[nx][self.right(ny)] = ">"
        # Advance south
        assert reqs == []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == "v" and self.data[self.down(i)][j] == ".":
                    reqs.append((i, j))
        changed += len(reqs)
        while reqs:
            nx, ny = reqs.pop()
            self.data[nx][ny] = "."
            self.data[self.down(nx)][ny] = "v"
        return changed

    def __str__(self):
        return "\n".join("".join(stuff) for stuff in self.data)

def create_board(inputname):
    gen = yield_line(inputname)
    lines = [list(line) for line in gen]
    board = Board(lines)
    return board

def solve(prob, inputname):
    board = create_board(inputname)

    if prob == 1:
        it = 1
        while board.advance() != 0:
            it += 1
        return it
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
