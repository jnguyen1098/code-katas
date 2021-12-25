#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

class Board:
    def __init__(self, data):
        self.data = data

    def advance(self):
        # Advance east
        # Advance west
        pass

    def __str__(self):
        return "\n".join("".join(stuff) for stuff in self.data)

def create_board(inputname):
    gen = yield_line(inputname)
    lines = [line for line in gen]
    board = Board(lines)
    return board

def solve(prob, inputname):
    board = create_board(inputname)

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
