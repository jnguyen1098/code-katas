#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def roll(pointer):
    result = pointer.data % 100
    pointer.data += 1
    return result

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(int(line[line.index(":") + 2:]))

    player_1 = lines[0]
    player_2 = lines[1]

    result = Pointer(1)

    print(player_1, player_2)

    print(f"{len(lines)} in the array")

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
