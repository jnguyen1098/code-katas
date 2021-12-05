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

def get_points(line):
    x1 = int(line.points[0][0])
    y1 = int(line.points[0][1])
    x2 = int(line.points[1][0])
    y2 = int(line.points[1][1])
    points = []
    print(x1, y1, x2, y2, end=" ")
    if x1 == x2:
        print("vertical")
        if y1 > y2:
            while y2 <= y1:
                print(f"    {x2},{y2}")
                points.append((x2, y2))
                y2 += 1
        else:
            while y1 <= y2:
                print(f"    {x1},{y1}")
                points.append((x1, y1))
                y1 += 1
    elif y1 == y2:
        print("horizontal")
        if x1 > x2:
            while x2 <= x1:
                print(f"    {x2},{y2}")
                points.append((x2, y2))
                x2 += 1
        else:
            while x1 <= x2:
                print(f"    {x1},{y1}")
                points.append((x1, y1))
                x1 += 1
    elif x1 - x2 == y1 - y2:
        return []
        print("diagonal pointing north east")
        if x1 < x2:
            while x1 != x2 and y1 != y2:
                print(f"    {x1},{y1}")
                points.append((x1, y1))
                x1 += 1
                y1 += 1
            print(f"    {x2},{y2}")
            points.append((x2, y2))
        elif x1 > x2:
            while x1 != x2 and y1 != y2:
                print(f"    {x2},{y2}")
                points.append((x2, y2))
                x2 += 1
                y2 += 1
            print(f"    {x1},{y1}")
            points.append((x1, y1))
        else:
            print("same point? lol")

    elif x1 - x2 == -(y1 - y2):
        return []
        print("diagonal pointing south east")
        if x1 < x2:
            while x1 != x2 and y1 != y2:
                print(f"    {x1},{y1}")
                points.append((x1, y1))
                x1 += 1
                y1 -= 1
            print(f"    {x2},{y2}")
            points.append((x2, y2))
        elif x1 > x2:
            while x1 != x2 and y1 != y2:
                print(f"    {x2},{y2}")
                points.append((x2, y2))
                x2 += 1
                y2 -= 1
            print(f"    {x1},{y1}")
            points.append((x1, y1))
        else:
            print("same point? lol")

    else:
        print("something else")
        exit()
            
    return points

for idx, line in enumerate(_lines):
    lines.append(Line(line))

for line in lines:
    print(line)

grid = []

length = 10

for i in range(length):
    grid.append([0] * length)

print()

points = []

for line in lines:
    points.append(get_points(line))

for point in points:
    for shit in point:
        print(shit)
        grid[shit[0]][shit[1]] += 1

for row in grid:
    print(row)
    
count = 0
for row in grid:
    for thing in row:
        if thing >= 2:
            count += 1
print(count)
