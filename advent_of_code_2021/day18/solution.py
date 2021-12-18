#!/usr/bin/env python3

import json
import sys
sys.path.append("..")

from ansi import *
from comp import *

def str_to_pair(string):
    arr = json.loads(string)
    return [arr[0], arr[1]]

def peek(string, i):
    return string[i + 1] if i + 1 < len(string) else None

def tokenize(string):
    pass

class SnailNum:
    def __init__(self, left, right):
        self.l = left
        self.r = right

    def __str__(self):
        return f"[ {self.l} , {self.r} ]"

    def __add__(self, other):
        return 0
        return SnailNum(str([json.loads(str(self)), json.loads(str(other))]))

    def __eq__(self, other):
        return str(self) == str(other)

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
    print(red(rev(f"Part 1")) + f": {solve(1, 'input')}\n")
    print(red(rev(f"Part 2")) + f": {solve(2, 'input')}\n")
