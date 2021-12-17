#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = []
        for i in range(rows):
            self.data.append(["."] * cols)

    def draw(self, x, y, symb):
        if self.data[x][y] != ".":
            print(f"{self.data[x][y]} is not a dot")
            exit(1)
        self.data[x][y] = symb

    def draw_rect(self, rel_x, rel_y, row_start, row_end, col_start, col_end):
        for i in range(row_start, row_end + 1):
            for j in range(col_start, col_end + 1):
                self.draw(i, j, "T")

    def __str__(self):
        result = []
        for row in self.data:
            result.append("".join(row))
        return "\n".join(result)

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

    print(f"x range is [{x_l}, {x_r}]")
    print(f"y range is [{y_l}, {y_r}]")

    # x is <-->
    # y is ^
    #      |
    #      v
    highest_y = -math.inf
    x_range = 100
    y_range = 100
    times = 100
    reached = False

    for i in range(x_range):
        for j in range(y_range):
            x_vel = i
            y_vel = j
            point = Point(x_vel, y_vel)
            highest_y = -math.inf
        
            #print("start", point)
            for i in range(times):
                point.step()
                highest_y = max(highest_y, point.y)
                #print(point)
                if within(point.x, point.y, int(x_l), int(x_r), int(y_l), int(y_r)):
                    reached = True
                    print(f"within! highest y is {highest_y}")
                    break

    if reached:
        print("highest ever is", highest_y)
    else:
        print("nothing ever hit lol")

    if prob == 1:
        return highest_y
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    """
    inputs = ["small", "example", "real"]
    expcts = [[10, 20, 30], [40, 50, 60]]
    """
    inputs = ["example", "real"]
    expcts = [[45, 30], [50, 60]]
    shortc = True

    for idx, part in enumerate(expcts):
        for filename, expected in zip(inputs, part):
            print(cya(rev(f"Filename: {filename}")))
            output = solve(idx + 1, filename)
            passed, msg = expect(output, expected)
            result = rev(grn("PASS") if passed else red("FAIL"))
            print(f"Part {idx + 1}: {output} {grn(msg) if passed else red(msg)}\n")
            if not passed and shortc: exit()
        print("\n" * 2)
