#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

MOD = 1000000007

inputname = "real"
inputname = "example"

letters = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdfeg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}

lines = open(inputname, "r").read().splitlines()

for idx, line in enumerate(lines):
    print(idx, line)
print("linecount:", len(lines))
