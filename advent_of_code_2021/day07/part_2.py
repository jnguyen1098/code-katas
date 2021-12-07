#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

MOD = 1000000007

tmp_data = [int(tmp) for tmp in open("input", "r").read().split(",")]
#tmp_data = [int(tmp) for tmp in open("example", "r").read().split(",")]

def move_all_to(crabs, num):
    cost = 0
    for i in range(len(crabs)):
        cost += abs(crabs[i] - num)
    return cost

min_cost = math.inf

for i in range(len(tmp_data)):
    min_cost = min(min_cost, move_all_to(tmp_data, i))

print(min_cost)
