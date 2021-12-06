#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

lines = open("input", "r").read().splitlines()

fish = [int(tmp) for tmp in lines[0].split(",")]

days = 80

for _ in range(days):
    for i in range(len(fish)):
        if fish[i] == 0:
            fish.append(8)
            fish[i] = 6
        else:
            fish[i] -= 1

print(len(fish))
