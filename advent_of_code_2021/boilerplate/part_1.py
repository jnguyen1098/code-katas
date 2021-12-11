#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

if __name__ == "__main__":
    inputname = "real"
    inputname = "example"
    inputname = "small"

    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(line)

    lines = [
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " "],
    ]

    start = (0, 0)
    for move in DIR.SURR:
        if new_point := point(start, move, 5, 5):
            lines[new_point[0]][new_point[1]] = "X"

    print_arr(lines, "|")

    print(f"{len(lines)} lines in the array")
