#!/usr/bin/env python3

import math

strings = [
    "cf",
    "acf",
    "bcdf",
    "acdeg",
    "acdfg",
    "abdfg",
    "abcefg",
    "abdefg",
    "abcdfg",
    "abcdefg",
]

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

class Line:
    def __init__(self, line):
        halves = line.split(" | ")
        self.facts = [list(word) for word in halves[0].split()]
        self.tests = [list(word) for word in halves[1].split()]
    def __str__(self):
        joined_facts = ["".join(word) for word in self.facts]
        joined_tests = ["".join(word) for word in self.tests]
        return f"{joined_facts} | {joined_tests}"

inputname = "example"
inputname = "real"
inputname = "small"

lines = open(inputname, "r").read().splitlines()

total = 0

for idx, line in enumerate(lines):
    print(Line(line))
