#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque, Counter
from bisect import bisect_left, bisect_right

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


MOD = 1000000007

inputname = "real"
inputname = "small"
inputname = "example"

MOVES = ((-1, -1), (-1, 0), (-1, 1),
         (0, -1),           (0, 1),
         (1, -1),  (1, 0),  (1, 1))

_lines = open(inputname, "r").read().splitlines()
grid = [[int(char) for char in line] for line in _lines]

def print_grid(grid):
    for i in grid:
        for j in i:
            print(j if j != 0 else bcolors.OKCYAN + str(j) + bcolors.ENDC, end="")
        print()
    print()

def incr_all(grid, rows, cols):
    num_flash = 0
    flashers = set()
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in flashers:
                grid[i][j] += 1
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] > 9:
                flashers.add((i, j))
    for x, y in flashers:
        for move in MOVES:
            new_x = x + move[0]
            new_y = y + move[1]
            if new_x >= 0 and new_x < rows and new_y >= 0 and new_y < cols:
                grid[new_x][new_y] += 1
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] > 9:
                num_flash += 1
                grid[i][j] = 0
    return num_flash

def advance(grid, rows, cols):
    return incr_all(grid, rows, cols)

total = 0
print_grid(grid)
for i in range(2):
    total += advance(grid, len(grid), len(grid[0]))
    print_grid(grid)
print(total)
