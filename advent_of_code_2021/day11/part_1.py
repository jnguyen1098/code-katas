#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque, Counter
from bisect import bisect_left, bisect_right

MOD = 1000000007

inputname = "real"
inputname = "example"

lines = open(inputname, "r").read().splitlines()

for idx, line in enumerate(lines):
    counter = Counter([int(chr) for chr in line])
    print(counter)
print("linecount:", len(lines))
