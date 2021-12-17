#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = []
        for i in range(rows):
            self.data.append(["."] * cols)

    def print(self):
        for row in self.data:
            print(row)

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(parse(r"target area: x=([^,]+), y=(.*)", line))

    x_l, x_r = lines[0][0].split("..")
    y_l, y_r = lines[0][1].split("..")

    print(f"x range is [{x_l}, {x_r}]")
    print(f"y range is [{y_l}, {y_r}]")

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    """
    inputs = ["small", "example", "real"]
    expcts = [[10, 20, 30], [40, 50, 60]]
    """
    inputs = ["example", "real"]
    expcts = [[20, 30], [50, 60]]
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
