#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

class Point:
    def __init__(self, x_vel, y_vel):
        self.x = 0
        self.y = 0
        self.x_vel = x_vel
        self.y_vel = y_vel
    def step(self):
        self.x += self.x_vel
        self.y += self.y_vel
        if self.x_vel > 0:
            self.x_vel -= 1
        elif self.x_vel < 0:
            self.x_vel += 1
        self.y_vel -= 1
    def __str__(self):
        return "\n".join(
            [f"x={self.x}", f"y={self.y}", f"x_vel={self.x_vel}", f"y_vel={self.y_vel}", ""]
        )

def within(x, y, x_l, x_r, y_l, y_r):
    return x_l <= x <= x_r and y_l <= y <= y_r

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(parse(r"target area: x=([^,]+), y=(.*)", line))

    x_l, x_r = lines[0][0].split("..")
    y_l, y_r = lines[0][1].split("..")

    global_highest_y = -math.inf
    reached = False

    vals = 0

    for i in range(300):
        for j in range(-300, 300):
            point = Point(i, j)
            highest_y = -math.inf
        
            while True:
                point.step()
                highest_y = max(highest_y, point.y)
                if within(point.x, point.y, int(x_l), int(x_r), int(y_l), int(y_r)):
                    reached = True
                    global_highest_y = max(global_highest_y, highest_y)
                    vals += 1
                    break
                elif point.x > int(x_r) or point.y < int(y_l):
                    break

    if prob == 1:
        return global_highest_y
    elif prob == 2:
        return vals
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputs = ["example", "real"]
    expcts = [[45, 11781], [112, 4531]]
    shortc = False

    for idx, part in enumerate(expcts):
        for filename, expected in zip(inputs, part):
            print(cya(rev(f"Filename: {filename}")))
            output = solve(idx + 1, filename)
            passed, msg = expect(output, expected)
            result = rev(grn("PASS") if passed else red("FAIL"))
            print(f"Part {idx + 1}: {output} {grn(msg) if passed else red(msg)}\n")
            if not passed and shortc: exit()
        print("\n" * 2)
