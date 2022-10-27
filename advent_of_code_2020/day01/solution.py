#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(line)

#    print_arr(lines)

#    print(f"{len(lines)} in the array")

    if prob == 1:
        nums = list(map(int, lines))
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == 2020:
                    return nums[i] * nums[j]
    elif prob == 2:
        nums = list(map(int, lines))
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                for k in range(j + 1, len(nums)):
                    if nums[i] + nums[j] + nums[k] == 2020:
                        return nums[i] * nums[j] * nums[k]
    else:
        print("Invalid problem code")
        exit()
