#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def solve(prob, inputname):

    rows = []
    for line in yield_line(inputname):
        rows.append(intgrid(line))
    print_arr(rows)

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputs = ["example", "real"]
    expcts = [[40, 30], [50, 60]]
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
