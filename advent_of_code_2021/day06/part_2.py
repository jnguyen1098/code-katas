#!/usr/bin/env python3

import sys
import math

from dataclasses import dataclass

lines = open("input", "r").read().splitlines()

fish = [int(tmp) for tmp in lines[0].split(",")]

from heapq import *

days = 18

reqs = []
result = []

for i in range(len(fish)):
    heappush(reqs, fish[i] + 1)
    result.append((fish[i] - days) % 7)

while reqs:
    print(heappop(reqs))

print(result)
print(len(result))

assert result == [6, 0, 6, 4, 5, 6, 0, 1, 1, 2, 6, 0, 1, 1, 1, 2, 2, 3, 3, 4, 6, 7, 8, 8, 8, 8]


