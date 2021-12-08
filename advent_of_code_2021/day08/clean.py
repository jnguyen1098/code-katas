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
    print()

def deduce_a(letters, models):
    two = None
    three = None
    for model in models:
        if len(model) == 2:
            two = model
        if len(model) == 3:
            three = model
    if not all([two, three]):
        print("could not find both 2 and 3")
        exit(1)


inputname = "small"
inputname = "example"

lines = open(inputname, "r").read().splitlines()

for idx, line in enumerate(lines):
    print(line)
    letters = {}
    model_line, test_line = line.split(" | ")
    models = [sorted(word) for word in model_line.split()]
    tests = [sorted(word) for word in test_line.split()]

    deduce_a(letters, models)

    print_map(letters)
