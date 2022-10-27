#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def get_row(sequence):
    l = 0
    r = 127

    try:
        assert len(sequence) == 10
    except:
        print("FAIL:", sequence)

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

    try:
        assert len(sequence) == 10
    except:
        print("FAIL:", sequence)

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
    mask = sequence.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1")
    while mask and mask[0] == "0":
        mask = mask.removeprefix("0")
    return 0 if not mask else int(mask, 2)
#    return get_row(sequence) * 8 + get_seat(sequence)

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        if line in ["", "\n"]:
            continue
        lines.append(line)

    if prob == 1:
        return max([get_id(seq) for seq in lines])
    elif prob == 2:
        numbers = set(list(range(1024)))

        for seq in lines:
            numbers.remove(get_id(seq))
        numbers = list(sorted(numbers))

        for i in range(1, len(numbers)):
            if numbers[i] - numbers[i - 1] > 1:
                return numbers[i]

        raise Exception("Couldn't find seat")
    else:
        print("Invalid problem code")
        exit()
