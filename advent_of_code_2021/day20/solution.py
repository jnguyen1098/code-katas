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

def relevant(image, x, y, rows, cols):
    for point in (
        (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)
    ):
        if thing := get_point((x, y), point, rows, cols):
            if image[thing[0]][thing[1]] == "#":
                return True
    return False

def solve(prob, inputname):
    print("file", inputname)
    lines = []
    gen = yield_line(inputname)

    tmp_gen = yield_line(inputname)
    next(tmp_gen)
    next(tmp_gen)
    dim = len(next(tmp_gen))
    expansion = 5
    new_len = dim + (expansion * 2)

    output = []
    for i in range(new_len):
        output.append(["."] * new_len)

    for i in range(expansion):
        lines.append(["."] * new_len)

    kernel = None

    for idx, line in enumerate(gen):
        if idx == 0: kernel = line[:]
        elif idx == 1: continue
        else:
            lines.append((["."] * expansion) + list(line) + (["."] * expansion))

    for i in range(expansion):
        lines.append(["."] * new_len)

    print_arr(lines)
    print()

    output2 = copy.deepcopy(output)
    assert len(lines) == len(lines[0]) and len(lines) == new_len

    print(f"first iteration bounds are [{expansion}, {new_len - expansion})")
    for i in range(expansion - 1, new_len - expansion + 1):
        for j in range(expansion - 1, new_len - expansion + 1):
            cnt = count(lines, i, j, new_len, new_len)
            if relevant(lines, i, j, new_len, new_len):
                output[i][j] = kernel[cnt]

    print("first output")
    print_arr(output)

    for i in range(expansion - 2, new_len - expansion + 2):
        for j in range(expansion - 2, new_len - expansion + 2):
            cnt = count(output, i, j, new_len, new_len)
            if relevant(output, i, j, new_len, new_len):
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
