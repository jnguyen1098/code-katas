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

def win(board, nums):
    tmp = copy.deepcopy(board)
    zop = zip(list(zip(*tmp)))
    for num in nums:
        mark(tmp, num)

    for row in tmp:
        if set(row) == set([-1]):
            return True

    for col in tmp:
        if set(col) == set([-1]):
            return True

    return False


MOD = 1000000007

delim = "\n"

lines = open("input", "r").read().splitlines()

numbers = [int(num) for num in lines[0].split(",")]

boards = []
b_i = -1

for idx, line in enumerate(lines):
#print(idx, line)
    if idx == 0: continue
    if line == "":
        b_i += 1
        boards.append([])
    else:
        row = [int(tmp) for tmp in line.split()]
        boards[b_i].append(row)

for board in boards:
    for row in board:
        print(row)
    print()

winset = set()

for i in range(len(numbers)):
    curr = numbers[:i+1]
    for board_idx, board in enumerate(boards):
       if win(board, curr):
           for num in curr:
               mark(board, num)
           #print(board, curr)
           finsum = 0
           for row in board:
               for num in row:
                   if num != -1:
                       finsum += num
           #print(finsum)
           if board_idx not in winset:
               print("win", board_idx)
               """
               for row in board:
                   print(row)
               """
               print(finsum * curr.pop())
               winset.add(board_idx)
