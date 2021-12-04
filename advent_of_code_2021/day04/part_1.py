#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

import copy

def mark(board, num):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == num:
                board[i][j] = -1

DISPLACEMENT = (0, 1, 2, 3, 4)

def win(board, nums):
    tmp = copy.deepcopy(board)
    for num in nums:
        mark(board, num)

    for row in board:
        if set(row) == set(-1):
            return True

    for i in range(5):
        symb = set()
        for disp in DISPLACEMENT:
            symb.add(board[i + disp][i])
        if symb == set(-1):
            return True

    return False


MOD = 1000000007

delim = "\n"

lines = open("input", "r").read().splitlines()

numbers = [int(num) for num in lines[0].split(",")]

for idx, line in enumerate(lines):
    print(line)
print("linecount:", len(lines))
