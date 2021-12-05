#!/usr/bin/env python3

from dataclasses import dataclass
import sys
import math

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
    if x1 == x2:
        if y1 > y2:
            while y2 <= y1:
                points.append((x2, y2))
                y2 += 1
        else:
            while y1 <= y2:
                points.append((x1, y1))
                y1 += 1
    elif y1 == y2:
        if x1 > x2:
            while x2 <= x1:
                points.append((x2, y2))
                x2 += 1
        else:
            while x1 <= x2:
                points.append((x1, y1))
                x1 += 1
    elif x1 - x2 == y1 - y2:
        if x1 < x2:
            while x1 != x2 and y1 != y2:
                points.append((x1, y1))
                x1 += 1
                y1 += 1
            points.append((x2, y2))
        elif x1 > x2:
            while x1 != x2 and y1 != y2:
                points.append((x2, y2))
                x2 += 1
                y2 += 1
            points.append((x1, y1))

    elif x1 - x2 == -(y1 - y2):
        if x1 < x2:
            while x1 != x2 and y1 != y2:
                points.append((x1, y1))
                x1 += 1
                y1 -= 1
            points.append((x2, y2))
        elif x1 > x2:
            while x1 != x2 and y1 != y2:
                points.append((x2, y2))
                x2 += 1
                y2 -= 1
            points.append((x1, y1))

    return points

for idx, line in enumerate(_lines):
    lines.append(Line(line))

grid = []

length = 1000

for i in range(length):
    grid.append([0] * length)

points = []

for line in lines:
    points.append(get_points(line))

for point in points:
    for shit in point:
        grid[shit[0]][shit[1]] += 1

count = 0
for row in grid:
    for thing in row:
        if thing >= 2:
            count += 1
print(count)
