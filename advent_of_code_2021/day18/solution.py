#!/usr/bin/env python3

import json
import sys
sys.path.append("..")

from ansi import *
from comp import *

class SnailNum:
    def __init__(self, string):
        tmp = json.loads(string)
        self.l = tmp[0]
        self.r = tmp[1]

    def __str__(self):
        return f"[ {self.l} , {self.r} ]"

    def __add__(self, other):
        return SnailNum(str([json.loads(str(self)), json.loads(str(other))]))

def solve(prob, inputname):
    numbers = [line for line in yield_line(inputname)]

    snail_numbers = [SnailNum(num) for num in numbers]

    for snail in snail_numbers:
        print(snail)

    base = snail_numbers[0]

    for i in range(1, len(snail_numbers)):
        base += snail_numbers[i]

    print(f"after adding: {base}")

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputs = ["add_test", "example", "real"]
    expcts = [[[[1, 2], [[3, 4], 5]], 20, 30], [40, 50, 60]]
    shortc = True

    for idx, part in enumerate(expcts):
        for filename, expected in zip(inputs, part):
            print(cya(rev(f"Filename: {filename}")))
            output = solve(idx + 1, filename)
            passed, msg = expect(output, expected)
            result = rev(grn("PASS") if passed else red("FAIL"))
            print(f"Part {idx + 1}: {output} {grn(msg) if passed else red(msg)}\n")
            if not passed and shortc: exit()
        print("\n" * 2)
