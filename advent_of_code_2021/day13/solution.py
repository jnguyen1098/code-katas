#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

class Paper:
    def __init__(self, dots, folds):
        self.dots = dots
        self.folds = folds
        self.data = []
        for row in range(max([dot[1] for dot in dots]) + 1):
            self.data.append(["."] * (max([dot[0] for dot in dots]) + 1))
        for dot in self.dots:
            self.draw_rm((dot[1], dot[0]), "#")

    def draw_rm(self, dot, symbol):
        self.data[dot[0]][dot[1]] = symbol

    def maintain_rows(self, x, y):
        self.data = self.data[x : y + 1]

    def maintain_cols(self, x, y):
        self.data = [self.data[i][x : y + 1] for i in range(len(self.data))]

    def _fold(self, axis, disp):
        if axis == "y":
            for i in range(disp, len(self.data)):
                for j in range(len(self.data[i])):
                    if self.data[i][j] == "#":
                        self.draw_rm((disp - (i - disp), j), "#")
            self.maintain_rows(0, disp - 1)
        elif axis == "x":
            for i in range(len(self.data)):
                for j in range(disp, len(self.data[i])):
                    if self.data[i][j] == "#":
                        self.draw_rm((i, (disp - (j - disp))), "#")
            self.maintain_cols(0, disp - 1)

    def fold(self, times):
        for i in range(times):
            self._fold(self.folds[0][0], int(self.folds[0][1]))
            self.folds.pop(0)
        return self.count_dots()

    def count_dots(self):
        dot_count = 0
        for row in self.data:
            dot_count += sum(map(lambda x: x == "#", row))
        return dot_count

    def __str__(self):
        return "\n".join(["".join(row) for row in self.data])

def solve(prob, inputname):
    dots = []
    folds = []
    gen = yield_line(inputname)

    for line in gen:
        if line == "": break
        dots.append(intsep(line, ","))

    for line in gen:
        folds.append(parse(r"fold along (\w)+=(\d+)", line))

    paper = Paper(dots, folds)

    if prob == 1:
        return paper.fold(1)
    elif prob == 2:
        paper.fold(len(paper.folds))
        print(paper)
        return 0
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputs = ["example", "real"]
    expcts = [[17, 621], [0, 0]]
    shortc = True

    for idx, part in enumerate(expcts):
        for filename, expected in zip(inputs, part):
            print(cya(rev(f"Filename: {filename}")))
            output = solve(idx + 1, filename)
            passed, msg = expect(output, expected)
            result = rev(grn("PASS") if passed else red("FAIL"))
            print(f"Part {idx + 1}: {output} {grn(msg) if passed else red(msg)}\n")
            if not passed and shortc: exit()
        print("\n" * 2)
