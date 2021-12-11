#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(line)

    print_arr(lines)

    print(f"{len(lines)} lines in the array")

    if prob == 1:
        return 10
    elif prob == 2:
        return 20
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputname = "real"
    inputname = "example"
    inputname = "small"

    output1 = solve(1, inputname)
    print(f"Problem 1: {output1}")

    output2 = solve(2, inputname)
    print(f"Problem 2: {output2}")
