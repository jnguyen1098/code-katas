#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

MOD = 1000000007

inputname = "example"
inputname = "real"

lines = open(inputname, "r").read().splitlines()

for idx, line in enumerate(lines):
    print(idx, line)
print("linecount:", len(lines))
