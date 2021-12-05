#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

MOD = 1000000007

delim = "\n"

lines = open("input", "r").read().splitlines()
comms = []

for idx, line in enumerate(lines):
    tmp = line.split(" -> ")
    comms.append((tmp[0], tmp[1]))

print(comms)
