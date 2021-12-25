#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

INSTRUCTIONS = set(["inp", "add", "sub", "mul", "div"])

class Instruction:
    def __init__(self, opcode, lop, rop):
        self.opcode = opcode
        self.lop = lop
        if rop.isalpha():
            self.rop = rop
        elif rop == "":
            self.rop = None
        else:
            self.rop = int(rop)
    def __str__(self):
        return f"{self.opcode} {self.lop} {self.rop if self.rop else ''}"

def get_char(string):
    for char in string:
        yield char

def simulate(instructions, input_stream, x=0, y=0, z=0):
    print(f"{input_stream=} {x=} {y=} {z=}")
    stream = get_char(input_stream)
    reg = {"w": 0, "x": x, "y": y, "z": z}
    for inst in instructions:
        match inst.opcode:
            case "inp":
                reg["w"] = int(next(stream))
            case "add":
                reg[inst.lop] += inst.rop if isinstance(inst.rop, int) else reg[inst.rop]
            case "eql":
                reg[inst.lop] = int(
                    (inst.lop if isinstance(inst.lop, int) else reg[inst.lop])
                        ==
                    (inst.rop if isinstance(inst.rop, int) else reg[inst.rop])
                )
            case "mod":
                reg[inst.lop] %= inst.rop if isinstance(inst.rop, int) else reg[inst.rop]
            case "mul":
                reg[inst.lop] *= inst.rop if isinstance(inst.rop, int) else reg[inst.rop]
            case "div":
                reg[inst.lop] //= inst.rop if isinstance(inst.rop, int) else reg[inst.rop]
    return reg["w"], reg["x"], reg["y"], reg["z"]

def chunk1(w, x=0, y=0, z=0):
    x = z % 26
    x += 11
    x = int (not int(x == w))
    y += 25
    y *= x
    y += 1
    z *= y
    y = w + 1
    y *= x
    z += y
    return w, x, y, z

def chunk2(w, z, x=0, y=0):
    x = z
    x %= 26
    x += 10
    if x == w:
        x = 1
    else:
        x = 0
    return w, x, y, z
    x = int(not x)
    y = 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 10
    y *= x
    z += y
    return w, x, y, z

def parse_instructions(inputname):
    instructions = []
    gen = yield_line(inputname)

    for line in gen:
        split = line.split()
        if len(split) == 3:
            instructions.append(Instruction(split[0], split[1], split[2]))
        else:
            instructions.append(Instruction(split[0], split[1], ""))

    return instructions

def solve(prob, inputname):

    instructions = parse_instructions(inputname)

    for line in instructions:
        print(line)

    simulate(instructions, "00000000000000")

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
