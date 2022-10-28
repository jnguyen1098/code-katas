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

        print(groups)

        for group in groups:
            total_sum += len(group)

        return total_sum

        return 0
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
