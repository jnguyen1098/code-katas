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

inputname = "small"
inputname = "example"
inputname = "real"

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
            elif j == -math.inf:
                print(bcolors.OKBLUE + "O" + bcolors.ENDC + " ", end="")
            elif j > 9:
                print(bcolors.FAIL + "X" + bcolors.ENDC + " ", end="")
            elif j <= 9:
                print(str(j) + " ", end="")
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

def get_new_flash(grid, rows, cols, old_flash):
    new_fls = get_flash(grid, rows, cols)
    return new_fls - old_flash

def flash(grid, rows, cols, fls):
    for x, y in fls:
        add_around_cell(grid, rows, cols, x, y, 1)
        grid[x][y] = -math.inf

def clean_board(grid, rows, cols):
    cnt = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == -math.inf:
                grid[i][j] = 0
                cnt += 1
    return cnt

def advance_and_get_flashes(grid, rows, cols):
    add_to_all_cells(grid, rows, cols, 1)
    while fls := get_flash(grid, rows, cols):
        flash(grid, rows, cols, fls)
    return clean_board(grid, rows, cols)

total = 0
print_grid(grid)
for i in range(100):
    total += advance_and_get_flashes(grid, len(grid), len(grid[0]))
    print_grid(grid)
print(total)
