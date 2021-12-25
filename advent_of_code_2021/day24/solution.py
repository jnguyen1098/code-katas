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

def simulate(instructions, input_stream):
    stream = get_char(input_stream)
    reg = {"w": 0, "x": 0, "y": 0, "z": 0}
    for inst in instructions:
        match inst.opcode:
            case "inp":
                reg["w"] = int(next(stream))
            case "add":
                reg[inst.lop] += inst.rop if isinstance(inst.rop, int) else reg[inst.rop]
            case "sub":
                reg[inst.lop] -= inst.rop if isinstance(inst.rop, int) else reg[inst.rop]
            case "mul":
                reg[inst.lop] *= inst.rop if isinstance(inst.rop, int) else reg[inst.rop]
            case "div":
                reg[inst.lop] //= inst.rop if isinstance(inst.rop, int) else reg[inst.rop]
    return reg["w"], reg["x"], reg["y"], reg["z"]

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
