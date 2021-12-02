#!/usr/bin/env python3

from collections import deque

delim = "\n"

lines = open("input", "r").read().splitlines()

for idx, line in enumerate(lines):
    print(idx, line)
print(len(lines))
