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
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()

def expect(actual, expected):
    if actual != expected:
        ret_msg = f"FAIL: {expected} but got {actual}"
        ret_sta = False
        return ret_sta, ret_msg
    return True, "PASS"

if __name__ == "__main__":
    inputs = ["small", "example", "real"]
    exp = [ [10, 20], [30, 40], [50, 60] ]

    for filename, expected in zip(inputs, exp):
        print(cya(rev(f"Filename: {filename}")))
        for tno in [1, 2]:
            output = solve(tno, filename)
            passed, msg = expect(output, expected[tno - 1])
            result = rev(grn("PASS") if passed else red("FAIL"))
            print(f"Part {tno}: {output} {grn(msg) if passed else red(msg)}")
        print("\n" * 2)
