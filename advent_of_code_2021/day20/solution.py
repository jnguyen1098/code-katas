#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def image_to_bin(string):
    return string.replace(" ", ".").replace(".", "0").replace("#", "1")

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
            if image[thing[0]][thing[1]] in ["#", "."]:
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
    expansion = 5 + (0 if prob == 1 else 200)
    new_len = dim + (expansion * 2)


    for i in range(expansion):
        lines.append(["."] * new_len)

    kernel = None

    for idx, line in enumerate(gen):
        if idx == 0: kernel = line[:]
        elif idx == 1: continue
        else:
            lines.append((["."] * expansion) + list(line) + (["."] * expansion))

    print("kernel", kernel)

    for i in range(expansion):
        lines.append(["."] * new_len)

    print_arr(lines)
    print()

    assert len(lines) == len(lines[0]) and len(lines) == new_len

    for it in range(2 if prob == 1 else 50):
        print("iteration", it, file=sys.stderr)
        output = []
        for i in range(new_len):
            output.append(["."] * new_len)
        for i in range(new_len):
            for j in range(new_len):
                cnt = count(lines, i, j, new_len, new_len)
                if relevant(lines, i, j, new_len, new_len):
                    output[i][j] = kernel[cnt]
        lines = output[:]
        print_arr(output)

    final_cnt = 0
    for i in range(50, new_len - 50):
        for j in range(50, new_len - 50):
            final_cnt += 1 if output[i][j] == "#" else 0

    return final_cnt
