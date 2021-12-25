#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *
from dataclasses import dataclass

@dataclass
class Instruction:
    opcode: str
    lop: str
    rop: str

INSTRUCTIONS = set(["inp", "add", "sub", "mul", "div"])

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        split = line.split()
        if len(split) == 3:
            lines.append(Instruction(split[0], split[1], split[2]))
        else:
            lines.append(Instruction(split[0], split[1], ""))

    for line in lines:
        print(line)

    print(f"{len(lines)} in the array")

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
