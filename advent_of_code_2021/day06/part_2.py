#!/usr/bin/env python3

import sys
import math

from dataclasses import dataclass

lines = open("input", "r").read().splitlines()

fish = [int(tmp) for tmp in lines[0].split(",")]

days = 80

reqs = []
result = []

for i in range(len(fish)):
    adder = 1
    while fish[i] + adder <= days:
        reqs.append(fish[i] + adder)
        adder += 7
    result.append((fish[i] - days) % 7)

while reqs:
    popped = reqs.pop()
    if popped == days:
        result.append(8)
        continue
    adder = 1
    tmp = popped + 8
    while tmp + adder <= days:
        reqs.append(tmp + adder)
        adder += 7
    if popped == days - 2:
        result.append(6)
    elif popped == days - 1:
        result.append(7)
    else:
        result.append(  (8 - (days - popped))  % 7)

print(len(result))
