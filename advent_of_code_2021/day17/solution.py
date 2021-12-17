#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def solve(prob, inputname):
    line = parse(r"target area: x=([^,]+), y=(.*)", open(inputname).read())

    x_l, x_r = line[0].split("..")
    y_l, y_r = line[1].split("..")

    global_highest_y = -math.inf
    reached = False

    vals = 0

    for i in range(300):
        for j in range(-300, 300):
            x, y = 0, 0
            x_v, y_v = i, j
            highest_y = -math.inf
        
            while True:
                x += x_v
                y += y_v
                x_v += 1 if x_v < 0 else -1 if x_v > 0 else 0
                y_v -= 1
                highest_y = max(highest_y, y)
                if int(x_l) <= x <= int(x_r) and int(y_l) <= y <= int(y_r):
                    reached = True
                    global_highest_y = max(global_highest_y, highest_y)
                    vals += 1
                    break
                elif x > int(x_r) or y < int(y_l):
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
