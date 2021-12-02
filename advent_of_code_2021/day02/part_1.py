#!/usr/bin/env python3

from collections import deque

delim = "\n"

fin = open("input", "r").read().split(delim)
lines = [line for line in fin]

print(len(lines))

x = 0
y = 0

for idx, line in enumerate(lines):
    try:
        direction = line.split(" ")[0]
        magnitude = line.split(" ")[1]
        print(idx, direction, magnitude)
        if direction == "down":
            x += int(magnitude)
        elif direction == "up":
            x -= int(magnitude)
        else:
            y += int(magnitude)
    except:
        pass

print(x, y)
