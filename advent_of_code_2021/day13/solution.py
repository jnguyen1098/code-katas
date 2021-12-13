#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

class Paper:
    def __init__(self, dots, folds):
        self.rows = max([dot[0] for dot in dots]) + 1
        self.cols = max([dot[1] for dot in dots]) + 1
        self.dots = dots
        self.folds = folds
        self.data = []
        for row in range(self.cols):
            self.data.append(["."] * self.rows)
        for dot in self.dots:
            self.draw_cm(dot, "#")

    def draw_cm(self, dot, symbol):
        self.data[dot[1]][dot[0]] = symbol

    def draw_rm(self, dot, symbol):
        self.data[dot[0]][dot[1]] = symbol

    def demo(self):
        # Colour in the first row
        for i in range(self.rows):
            self.data[0][i] = "x"
        # Colour in the first col
        for i in range(self.cols):
            self.data[i][0] = "o"

    def maintain_rows(self, x, y):
        """Inclusive-Inclusive."""
        self.data = copy.deepcopy(self.data[x : y + 1])

    def maintain_cols(self, x, y):
        tmp_row = []
        for i in range(len(self.data)):
            tmp_row.append(self.data[i][x : y + 1])
        self.data = tmp_row

    def fold(self, axis, disp):
        if axis == "y":
            for i in range(disp, len(self.data)):
                for j in range(len(self.data[i])):
                    if self.data[i][j] == "#":
                        self.draw_rm((disp - (i - disp), j), "#")
            self.maintain_rows(0, disp - 1)
        elif axis == "x":
            self.maintain_cols(0, disp - 1)
        else:
            print("Bad input", axis, disp)
            exit()

    def count_dots(self):
        dot_count = 0
        for row in self.data:
            for char in row:
                if char == "#":
                    dot_count += 1
        return dot_count

    def __str__(self):
        rep = []
        for row in self.data:
            rep.append("".join(row))
        return "\n".join(rep)

def solve(prob, inputname):
    dots = []
    folds = []
    gen = yield_line(inputname)

    for line in gen:
        if line == "": break
        dots.append(intsep(line, ","))

    for line in gen:
        folds.append(parse(r"fold along (\w)+=(\d+)", line))

    print_arr(dots, " ")
    print()
    print_arr(folds, " ")
    print()
    paper = Paper(dots, folds)
    print(paper, "\n")

    if prob == 1:
        paper.fold(paper.folds[0][0], int(paper.folds[0][1]))
        print(paper, "\n")
        paper.fold(paper.folds[1][0], int(paper.folds[1][1]))
        return paper.count_dots()
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputs = ["example", "real"]
    expcts = [[17, 30], [50, 60]]
    shortc = True

    for idx, part in enumerate(expcts):
        for filename, expected in zip(inputs, part):
            print(cya(rev(f"Filename: {filename}")))
            output = solve(idx + 1, filename)
            passed, msg = expect(output, expected)
            result = rev(grn("PASS") if passed else red("FAIL"))
            print(f"Part {idx + 1}: {output} {grn(msg) if passed else red(msg)}\n")
            exit()
            if not passed and shortc: exit()
        print("\n" * 2)
