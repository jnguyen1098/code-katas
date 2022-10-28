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
        state_stack = [0]

        while True:
            if (new_state := get_next_state(state))[0] in states:
                break
            state_stack.append(new_state[0])
            states.add(new_state[0])
            state = new_state

        nop_sled = None

        last_inst, last_val = code[-1]
        if last_inst in ["nop", "acc"] or (last_inst, last_val) == ("jmp", 1):
            nop_sled = len(code) - 1

        assert nop_sled is not None

        jmps = []

        for visited_idx in state_stack:
            if code[visited_idx][0] != "jmp":
                continue
            jmps.append(visited_idx)

        def loops(idx):
            state = (0, 0)  # program counter, accumulator

            code[idx] = ("nop", code[idx][1])

            states = set([0])
            state_stack = [0]

            while True:
                if state[0] == nop_sled:
                    return state[1] + (code[nop_sled][1] if code[nop_sled][0] == "acc" else 0)
                if (new_state := get_next_state(state))[0] in states:
                    code[idx] = ("jmp", code[idx][1])
                    return -1
                state_stack.append(new_state[0])
                states.add(new_state[0])
                state = new_state

        for idx in jmps:
            if (attempt := loops(idx)) != -1:
                return attempt

        raise Exception("Should not have exited loop")

    else:
        print("Invalid problem code")
        exit()
