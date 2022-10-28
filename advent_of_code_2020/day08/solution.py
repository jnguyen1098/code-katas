#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def solve(prob, inputname):
    code = []
    gen = yield_line(inputname)

    for line in gen:
        if line == "":
            continue
        inst, val = parse(r"(nop|acc|jmp) ([\-\+]\d+)", line)
        code.append((inst, int(val)))

    if prob == 1:

        def get_next_state(state):
            pc, cum = state

            inst, val = code[pc]
            if inst == "nop":
                return (pc + 1, cum)
            if inst == "acc":
                return (pc + 1, cum + val)
            if inst == "jmp":
                return (pc + val, cum)
            raise Exception(f"Invalid state {state} yielded {inst=} {val=}")

        state = (0, 0)  # program counter, accumulator

        states = set([0])
        while True:
            if (new_state := get_next_state(state))[0] in states:
                return state[1]
            states.add(new_state[0])
            state = new_state
        
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
