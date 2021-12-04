#!/usr/bin/env python3

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
        location = self.idx.get(num)
        if location:
            self.rows[location[0]][location[1]] = mark

    def win(self):
        for row in self.rows:
            if set(row) == set([-1]):
                return True
        for col in list(zip(*self.rows)):
            if set(col) == set([-1]):
                return True
        return False

    def get_score(self, winning_move):
        score = 0
        for row in self.rows:
            for num in row:
                if num != -1:
                    score += num
        return score * winning_move

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

wins = set()

for num in numbers:
    for idx, board in enumerate(boards):
        if idx in wins: continue
        board.mark(num, -1)
        if board.win():
            wins.add(idx)
            print(f"{idx} won on {num}")
            print(board)
            print(f"score: {board.get_score(num)}")
            print()
