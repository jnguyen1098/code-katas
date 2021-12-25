#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

class Board:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "\n".join("".join(stuff) for stuff in self.data)

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(list(line))

    board = Board(lines)
    print(board)

    print(f"{len(lines)} in the array")

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
