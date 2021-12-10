#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

MOD = 1000000007

inputname = "real"
inputname = "example"

correct = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

_correct = {v: k for k, v in correct.items()}

errorscore = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

lines = open(inputname, "r").read().splitlines()

stack = []

score = 0

newlines = []

for idx, line in enumerate(lines):
    bad = False
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            popped = stack.pop()
            if popped != _correct[char]:
                bad = True
                print("Error", char)
                score += errorscore[char]
    if not bad:
        newlines.append(line)

print(score)
        
for line in newlines:
    print(line)
