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

    tmp_gen = yield_line(inputname)
    next(tmp_gen)
    next(tmp_gen)
    dim = len(next(tmp_gen))
    new_len = dim + 5 + 5

    output = []
    for i in range(new_len):
        output.append(["."] * new_len)

    for i in range(5):
        lines.append(["."] * new_len)

    kernel = None

    for idx, line in enumerate(gen):
        if idx == 0: kernel = line[:]
        elif idx == 1: continue
        else:
            lines.append((["."] * 5) + list(line) + (["."] * 5))

    for i in range(5):
        lines.append(["."] * new_len)

    print_arr(lines)
    print()

    output2 = copy.deepcopy(output)

    for i in range(4, len(lines) - 4):
        for j in range(4, len(lines[i]) - 4):
            cnt = count(lines, i, j, len(lines), len(lines[i]))
            output[i][j] = kernel[cnt]

    print("first output")
    print_arr(output)

    for i in range(3, len(output) - 3):
        for j in range(3, len(output[i]) - 3):
            cnt = count(output, i, j, len(output), len(output[i]))
            output2[i][j] = kernel[cnt]

    print("second output")
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
