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
    1: "cf",
    7: "acf",
    4: "bcdf",
    2: "acdeg",
    3: "acdfg",
    5: "abdfg",
    0: "abcefg",
    6: "abdefg",
    9: "abcdfg",
    8: "abcdefg",
}

digit = {
    "cf": 1,
    "acf": 7,
    "bcdf": 4,
    "acdeg": 2,
    "acdfg": 3,
    "abdfg": 5,
    "abcefg": 0,
    "abdefg": 6,
    "abcdfg": 9,
    "abcdefg": 8,
}

lines = open(inputname, "r").read().splitlines()

for line in lines:
    left, right = line.split(" | ")
    signals = left.split()
    result = right.split()
    print(signals)
    print(result)
    print()
