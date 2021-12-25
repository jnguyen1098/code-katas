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
                print("add")
#reg[inst.lop] = inst.rop
            case "sub":
                print("subtract")
            case "mul":
                print("multiply")
            case "div":
                print("divide")

def solve(prob, inputname):
    instructions = []
    gen = yield_line(inputname)

    for line in gen:
        split = line.split()
        if len(split) == 3:
            instructions.append(Instruction(split[0], split[1], split[2]))
        else:
            instructions.append(Instruction(split[0], split[1], ""))

    for line in instructions:
        print(line)

    simulate(instructions, "1234567890")

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
