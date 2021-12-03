#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

MOD = 1000000007

delim = "\n"

lines = open("input", "r").read().splitlines()

def get_counts(lins):
    ones = [0] * 12
    zers = [0] * 12

    for line in lins:
        for idx, char in enumerate(line):
            if char == "0":
                zers[idx] += 1
            elif char == "1":
                ones[idx] += 1
            else:
                print("error")
                exit()
    return ones, zers

def fuck(lins, c1, c2):
    candidates = lins[:]

    for i in range(12):
        if len(candidates) == 1:
            break
        new_cans = []
        ones, zers = get_counts(candidates)
        mask = [c1 if ones[i] >= zers[i] else c2 for i in range(12)] # first
        for candidate in candidates:
            if candidate[i] == mask[i]:
                new_cans.append(candidate)
        candidates = new_cans
    return int(candidates.pop(), 2)

print(fuck(lines, "1", "0") * fuck(lines, "0", "1"))
