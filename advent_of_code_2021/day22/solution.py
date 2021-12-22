#!/usr/bin/env python3

import itertools
import json
import sys
sys.path.append("..")

from ansi import *
from comp import *

def get_cubes(xl, xr, yl, yr, zl, zr):
    x_range = [i for i in range(xl, xr + 1)]
    y_range = [i for i in range(yl, yr + 1)]
    z_range = [i for i in range(zl, zr + 1)]
    for product in itertools.product(x_range, y_range, z_range):
        yield product

def valid_line(xl, xr, yl, yr, zl, zr, direction):
    if xl < -50 and xr < -50: return False
    if xl > +50 and xr > +50: return False
    if yl < -50 and yr < -50: return False
    if yl > +50 and yr > +50: return False
    if zl < -50 and zr < -50: return False
    if zl > +50 and zr > +50: return False
    return True

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(
            parse(
                r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)",
                line
            )
        )

    for i in range(len(lines)):
        operation = lines[i][0]
        lines[i] = list(map(int, lines[i][1:])) + [operation]

    lines = [line for line in lines if valid_line(*line)]

    room = set()

    for line in lines:
        cubes = set(get_cubes(line[0], line[1], line[2], line[3], line[4], line[5]))
        if line[-1] == "on":
            for cube in cubes:
                room.add(cube)
        elif line[-1] == "off":
            for cube in cubes:
                room.discard(cube)

    if prob == 1:
        return len(room)
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
