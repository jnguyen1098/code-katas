#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

MOD = 1000000007

delim = "\n"

lines = open("input", "r").read().splitlines()

ones = [0] * 12
zers = [0] * 12

for idx, line in enumerate(lines):
    for idx, char in enumerate(line):
        if char == "0":
            zers[idx] += 1
        elif char == "1":
            ones[idx] += 1
        else:
            print("error")
            exit()

for i in range(len(ones)):
    print("0" if zers[i] > ones[i] else "1", end="")

print()

for i in range(len(ones)):
    print("1" if zers[i] > ones[i] else "0", end="")

print()

print("linecount:", len(lines))
