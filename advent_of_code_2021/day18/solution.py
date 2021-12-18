#!/usr/bin/env python3

import json
import sys
sys.path.append("..")

from ansi import *
from comp import *

def str_to_pair(string):
    arr = json.loads(string)
    return [arr[0], arr[1]]

class SnailNum:
    def __init__(self, left, right):
        if isinstance(left, SnailNum):
            print("this is a snailnum")

    def __str__(self):
        return ""
        return f"[ {self.l} , {self.r} ]"

    def __add__(self, other):
        return 0
        return SnailNum(str([json.loads(str(self)), json.loads(str(other))]))

def solve(prob, inputname):
    numbers = [line for line in yield_line(inputname)]

    snail_numbers = [SnailNum(num, 1) for num in numbers]

    base = snail_numbers[0]

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputs = ["add_test", "example", "real"]

    for i in [1, 2]:
        print(red(rev(f"Part {i}\n")))
        for filename in inputs:
            print("    " + cya(rev(f"Filename: {filename}")))
            output = solve(i, filename)
            print(f"        Output: {output}")
            print("\n" * 2)
