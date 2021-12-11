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
            if j == 0:
                print(bcolors.OKCYAN + str(j) + bcolors.ENDC + " ", end="")
            elif j <= 9:
                print(str(j) + " ", end="")
            elif j > 9:
                print(bcolors.FAIL + "X" + bcolors.ENDC + " ", end="")
            else:
                print("broken")
                exit()
        print()
    print()


def add_to_all_cells(grid, rows, cols, amt):
    for i in range(rows):
        for j in range(cols):
            grid[i][j] += amt

def get_flash(grid, rows, cols):
    fls = set()
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] > 9:
                fls.add((i, j))
    return fls

def advance_and_get_flashes(grid, rows, cols):
    add_to_all_cells(grid, rows, cols, 1)
    fls = get_flash(grid, rows, cols)
    return len(fls)

total = 0
print_grid(grid)
for i in range(2):
    total += advance_and_get_flashes(grid, len(grid), len(grid[0]))
    print_grid(grid)
print(total)
