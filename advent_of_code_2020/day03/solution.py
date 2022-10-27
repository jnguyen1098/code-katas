#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def displace(rows, cols, x, y, dx, dy):
    return ((x + dx) % rows, (y + dy) % cols)

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(line)

    if prob == 1:

        x, y = 0, 0
        count = 0

        rows = len(lines)
        cols = len(lines[0])

        while x < rows:
            if lines[x][y] == "#":
                count += 1
            if x == rows - 1:
                break
            x, y = displace(rows, cols, x, y, 1, 3)

        return count

    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
