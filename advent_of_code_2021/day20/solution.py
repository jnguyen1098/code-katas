#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def image_to_bin(string):
    return string.replace(".", "0").replace("#", "1")

def bin_to_int(string):
    return int(string, 2)

def image_to_int(string):
    return bin_to_int(image_to_bin(string))

def solve(prob, inputname):
    print("file", inputname)
    lines = []
    gen = yield_line(inputname)

    for i in range(10):
        lines.append(["."] * 15)

    for idx, line in enumerate(gen):
        if idx == 0: print("kernel", line)
        elif idx == 1: continue
        else:
            lines.append((["."] * 5) + [line] + (["."] * 5))

    for i in range(10):
        lines.append(["."] * 15)

    print_arr(lines)

    print(f"{len(lines)} in the array")

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
