#!/usr/bin/env python3

# 911 1991
# 984716 1991

from collections import deque

delim = "\n"

fin = open("input", "r").read().split(delim)
lines = [line for line in fin]

print(len(lines))

x = 0
y = 0

aim = 0

for idx, line in enumerate(lines):
    try:
        direction = line.split(" ")[0]
        magnitude = line.split(" ")[1]
        print(idx, direction, magnitude)
        if direction == "down":
            aim += int(magnitude)
        elif direction == "up":
            aim -= int(magnitude)
        else:
            y += int(magnitude)
            x += aim * int(magnitude)
    except:
        pass

print(x, y)
