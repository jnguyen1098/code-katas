#!/usr/bin/env python3

import math
import sys

sys.path.append("..")

from ansi import *

class Grid:
    def __init__(self, filename, sentinel):
        lines = open(filename, "r").read().splitlines()
        self.grid = [[int(char) for char in line] for line in lines]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.sentinel = sentinel

    def __str__(self):
        result = []
        for row in self.grid:
            row_line = []
            for char in row:
                row_line.append(bold(char) if char == 0 else dim(char))
            result.append("".join(row_line))
        result.append("")
        return "\n".join(result)

    def add_to_all_cells(self, amount):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] += amount

    def add_around_cell(self, x, y, amount):
        MOVES = ((-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1),  (1, 0),  (1, 1),)
        for move in MOVES:
            new_x = x + move[0]
            new_y = y + move[1]
            if new_x >= 0 and new_x < self.rows and new_y >= 0 and new_y < self.cols:
                self.grid[new_x][new_y] += amount

    def get_flash(self):
        fls = set()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] > 9:
                    fls.add((i, j))
        return fls

    def get_new_flash(self, old_flash):
        return self.get_flash() - old_flash

    def flash(self, fls):
        for x, y in fls:
            self.add_around_cell(x, y, 1)
            self.grid[x][y] = self.sentinel

    def clean_board(self):
        cnt = 0
        for i in range(self.rows):
           for j in range(self.cols):
                if self.grid[i][j] == self.sentinel:
                    self.grid[i][j] = 0
                    cnt += 1
        return cnt

    def advance_and_get_flashes(self):
        self.add_to_all_cells(1)
        while fls := self.get_flash():
            self.flash(fls)
        return self.clean_board()

