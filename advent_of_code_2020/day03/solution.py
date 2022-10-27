#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def displace(rows, cols, x, y, dx, dy):
    return ((x + dx) % rows, (y + dy) % cols)

def analyze(lines, dx, dy):
    x, y = 0, 0
    count = 0

    rows = len(lines)
    cols = len(lines[0])

    while x < rows:
        if lines[x][y] == "#":
            count += 1
        if x == rows - 1:
            break
        x, y = displace(rows, cols, x, y, dx, dy)

    return count

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(line)

    if prob == 1:
        return analyze(lines, 1, 3)

    elif prob == 2:
        return analyze(lines, 1, 1) * analyze(lines, 1, 3) * analyze(lines, 1, 5) * analyze(lines, 1, 7) * analyze(lines, 2, 1)
    else:
        print("Invalid problem code")
        exit()
