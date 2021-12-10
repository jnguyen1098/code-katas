#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

MOD = 1000000007

inputname = "example"
inputname = "real"

correct = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

_correct = {v: k for k, v in correct.items()}

errorscore = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

lines = open(inputname, "r").read().splitlines()

stack = []

score = 0

for idx, line in enumerate(lines):
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            popped = stack.pop()
            if popped != _correct[char]:
                print("Error", char)
                score += errorscore[char]
        
print(score)
