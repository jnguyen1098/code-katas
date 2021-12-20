#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def image_to_bin(string):
    return string.replace(".", "0").replace("#", "1")

def bin_to_int(string):
    return int(string, 2)

def image_to_int(string):
    return bin_to_int(image_to_bin(string))

def count(image, x, y, rows, cols):
    binmask = []
    for point in (
        (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)
    ):
        if thing := get_point((x, y), point, rows, cols):
            binmask.append(image[thing[0]][thing[1]])
    return image_to_int("".join(binmask))

def solve(prob, inputname):
    print("file", inputname)
    lines = []
    gen = yield_line(inputname)

    output = []
    for i in range(15):
        output.append(["."] * 15)

    for i in range(5):
        lines.append(["."] * 15)

    kernel = None

    for idx, line in enumerate(gen):
        if idx == 0: kernel = line[:]
        elif idx == 1: continue
        else:
            lines.append((["."] * 5) + list(line) + (["."] * 5))

    for i in range(5):
        lines.append(["."] * 15)

    print_arr(lines)
    print()

    output2 = copy.deepcopy(output)

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            cnt = count(lines, i, j, len(lines), len(lines[i]))
            output[i][j] = kernel[cnt]

    print()
    print_arr(output)

    for i in range(len(output)):
        for j in range(len(output[i])):
            cnt = count(output, i, j, len(output), len(output[i]))
            output2[i][j] = kernel[cnt]

    print()
    print_arr(output2)

    final_cnt = 0
    for i in range(len(output2)):
        for j in range(len(output2[0])):
            final_cnt += 1 if output2[i][j] == "#" else 0

    if prob == 1:
        return final_cnt
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
