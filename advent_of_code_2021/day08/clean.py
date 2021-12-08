#!/usr/bin/env python3

import math

"""
letters = {
    1: "cf",
    7: "acf",
    4: "bcdf",
    2: "acdeg",
    3: "acdfg",
    5: "abdfg",
    0: "abcefg",
    6: "abdefg",
    9: "abcdfg",
    8: "abcdefg",
}

digit = {
    "cf": 1,
    "acf": 7,
    "bcdf": 4,
    "acdeg": 2,
    "acdfg": 3,
    "abdfg": 5,
    "abcefg": 0,
    "abdefg": 6,
    "abcdfg": 9,
    "abcdefg": 8,
}
"""

def print_map(translate):
    for letter in "abcdefg":
        result = translate.get(letter)
        print(f"{letter}: {result}")

inputname = "small"

lines = open(inputname, "r").read().splitlines()

for idx, line in enumerate(lines):
    letters = {}
    model_line, test_line = line.split(" | ")
    models = model_line.split()
    tests = test_line.split()

    # Do trivial deduction
    for model in models:
        if len(model) == 2:
            letters["c"] = model[0]
            letters["f"] = model[1]
        elif len(model) == 3:
            letters["a"] = model[0]
            letters["c"] = model[1]
            letters["f"] = model[2]
        elif len(model) == 4:
            letters["b"] = model[0]
            letters["c"] = model[1]
            letters["d"] = model[2]
            letters["f"] = model[3]

    print_map(letters)
