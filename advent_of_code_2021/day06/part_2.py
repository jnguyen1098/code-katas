#!/usr/bin/env python3

import sys
import math

from dataclasses import dataclass
from timeit import default_timer as timer

lines = open("input", "r").read().splitlines()

fish = [int(tmp) for tmp in lines[0].split(",")]

days = 256

reqs = []
result = 0

minnum = math.inf

for i in range(len(fish)):
    adder = 1
    while fish[i] + adder <= days:
        reqs.append(fish[i] + adder)
        adder += 7
    result += 1

last_time = timer()

while reqs:
    popped = reqs.pop()
    if popped < minnum:
        curr = timer()
        print(f"{popped} -> {curr - last_time}")
        last_time = curr
        minnum = popped
    if popped == days:
        result += 1
        continue
    adder = 1
    tmp = popped + 8
    while tmp + adder <= days:
        reqs.append(tmp + adder)
        adder += 7
    result += 1

print(f"x -> {timer() - last_time}")

print(result)
