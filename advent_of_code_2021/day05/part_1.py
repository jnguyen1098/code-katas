#!/usr/bin/env python3

from dataclasses import dataclass
import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

MOD = 1000000007

delim = "\n"

_lines = open("input", "r").read().splitlines()
lines = []

@dataclass
class Line:
    def __init__(self, line):
        tmp = line.split(" -> ")
        self.points = [tmp[0].split(","), tmp[1].split(",")]
    def __str__(self):
        return f"{self.points}"

for idx, line in enumerate(_lines):
    lines.append(Line(line))

for line in lines:
    print(line)
