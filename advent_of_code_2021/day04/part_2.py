#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

import copy

def mark(board, num):
    cpy = copy.deepcopy(board)
    for i in range(len(cpy)):
        for j in range(len(cpy[i])):
            if cpy[i][j] == num:
                cpy[i][j] = -1
                return cpy
    return cpy

def win(board, nums):
    zop = list(zip(*board))
    for num in nums:
        board = mark(board, num)

    for row in board:
        if set(row) == set([-1]):
            return True

    for col in zop:
        if set(col) == set([-1]):
            return True

    return False

lines = open("input", "r").read().splitlines()

numbers = [int(num) for num in lines[0].split(",")]

boards = []
b_i = -1

for idx, line in enumerate(lines):
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
last_win = None

for i in range(len(numbers)):
    curr = numbers[:i+1]
    for board_idx, board in enumerate(boards):
       if win(board, curr):
           cpy = copy.deepcopy(board)
           for num in curr:
               cpy = mark(cpy, num)
           #print(board, curr)
           finsum = 0
           for row in cpy:
               for num in row:
                   if num != -1:
                       finsum += num
           #print(finsum)
           if board_idx not in winset:
               print("win", board_idx)
               for row in cpy:
                   print(row)
               print(finsum * curr.pop())
               winset.add(board_idx)
               last_win = board_idx
           """
           print(curr)
           """

def get_score(board, last):
    score = 0
    for row in board:
        for num in row:
            if num != -1:
                score += num
    return score * last

print("investigate last")
already_won = False
for i in range(len(numbers)):
    curr = numbers[:i+1]
    board_idx = last_win
    if already_won:
        exit()
    tmp = copy.deepcopy(boards[board_idx])
    for num in curr:
        tmp = mark(tmp, num)
    already_won = win(tmp, curr)
    print("win" if already_won else "", end="")
    print("", curr[-1])
    for row in tmp:
        print(row)
    print(curr)
    print("score:", get_score(tmp, curr[-1]))
    print()
    print()
    print()
