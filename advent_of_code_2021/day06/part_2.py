#!/usr/bin/env python3

import sys
import math

from dataclasses import dataclass

lines = open("input", "r").read().splitlines()

fish = [int(tmp) for tmp in lines[0].split(",")]

days = 80

reqs = []
result = 0

for i in range(len(fish)):
    adder = 1
    while fish[i] + adder <= days:
        reqs.append(fish[i] + adder)
        adder += 7
    result += 1

while reqs:
    popped = reqs.pop()
    if popped == days:
        result += 1
        continue
    adder = 1
    tmp = popped + 8
    while tmp + adder <= days:
        reqs.append(tmp + adder)
        adder += 7
    if popped == days - 2:
        result += 1
    elif popped == days - 1:
        result += 1
    else:
        result += 1

print(result)
