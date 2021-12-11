#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque, Counter
from bisect import bisect_left, bisect_right

MOD = 1000000007

inputname = "real"
inputname = "example"

_lines = open(inputname, "r").read().splitlines()
grid = [[int(char) for char in line] for line in _lines]

def print_grid(grid):
    for i in grid:
        print(i)
    print()

def advance(grid, rows, cols):
    pass

print_grid(grid)
for i in range(2):
    advance(grid, len(grid), len(grid[0]))
    print_grid(grid)
