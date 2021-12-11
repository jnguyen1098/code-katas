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

def add_around_cell(grid, rows, cols, x, y, amt):
    for move in MOVES:
        new_x = x + move[0]
        new_y = y + move[1]
        if new_x >= 0 and new_x < rows and new_y >= 0 and new_y < cols:
            grid[new_x][new_y] += amt

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
    for x, y in fls:
        add_around_cell(grid, rows, cols, x, y, 1)
    fls = get_flash(grid, rows, cols)
    return len(fls)

lmao = [[6,5,9,4,2,5,4,3,3,4],
[3,8,5,6,9,6,5,8,2,2],
[6,3,7,5,6,6,7,2,8,4],
[7,2,5,2,4,4,7,2,5,7],
[7,4,6,8,4,9,6,5,8,9],
[5,2,7,8,6,3,5,7,5,6],
[3,2,8,7,9,5,2,8,3,2],
[7,9,9,3,9,9,2,2,4,5],
[5,9,5,7,9,5,9,6,6,5],
[6,3,9,4,8,6,2,6,3,7],]

total = 0
print_grid(grid)
for i in range(2):
    total += advance_and_get_flashes(grid, len(grid), len(grid[0]))
    if i == 0 and grid != lmao:
        print("not ok")
        exit()
    print_grid(grid)
print(total)
