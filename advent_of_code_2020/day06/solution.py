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

    if prob == 1:

        assert lines[0] != ""

        groups = []
        curr_group = set()

        for line in lines:
            if line == "":
                groups.append(sorted(list(curr_group)))
                curr_group.clear()
                continue
            for char in line:
                curr_group.add(char)

        total_sum = 0

        for group in groups:
            total_sum += len(group)

        return total_sum

    elif prob == 2:

        assert lines[0] != ""

        groups = []
        curr_group = set()
        reset = True

        for line in lines:
            if reset:
                curr_group = set([char for char in line])
                reset = False
            if line == "":
                groups.append(sorted(list(curr_group)))
                curr_group.clear()
                reset = True
                continue
            tmp_set = set()
            for char in line:
                tmp_set.add(char)
            curr_group &= tmp_set

        total_sum = 0

        for group in groups:
            total_sum += len(group)

        return total_sum
    else:
        print("Invalid problem code")
        exit()
