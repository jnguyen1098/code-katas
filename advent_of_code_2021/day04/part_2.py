#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

import copy

lines = open("input", "r").read().splitlines()

numbers = [int(num) for num in lines[0].split(",")]

boards = []

class Board:

    def __init__(self, rows):
        self.rows = copy.deepcopy(rows)
        self.idx = {}
        for i in range(len(self.rows)):
            for j in range(len(self.rows[i])):
                self.idx[self.rows[i][j]] = (i, j)

    def mark(self, num, mark):
        location = self.idx[num]
        self.rows[location[0]][location[1]] = mark

    def __str__(self):
        return "\n".join(str(row) for row in self.rows)

tmp = []
for idx, line in enumerate(lines):
    if idx == 0: continue
    if line == "":
        if tmp != []:
            boards.append(Board(tmp))
            tmp.clear()
    else:
        row = [int(_tmp) for _tmp in line.split()]
        tmp.append(row)

for idx, board in enumerate(boards):
    print(idx)
    print(board)
    print()
