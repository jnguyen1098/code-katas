#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def get_row(sequence):
    l = 0
    r = 127

    for i in range(7):
        mid = l + (r - l) // 2
        if sequence[i] == "F":
            r = max(0, mid - 1)
        elif sequence[i] == "B":
            l = min(127, mid + 1)
        else:
            raise Exception(f"forbidden row symbol {sequence[i]}")

    return math.ceil(l + (r - l) / 2)

def get_seat(sequence):
    l = 0
    r = 7

    for i in range(7, 10):
        mid = l + (r - l) // 2
        if sequence[i] == "L":
            r = max(0, mid - 1)
        elif sequence[i] == "R":
            l = min(127, mid + 1)
        else:
            raise Exception(f"forbidden seat symbol {sequence[i]}")

    return math.ceil(l + (r - l) / 2)

def get_id(sequence):
    return get_row(sequence) * 8 + get_seat(sequence)
        

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(line)

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
