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

inputname = "example"
inputname = "real"
inputname = "small"

lines = open(inputname, "r").read().splitlines()

total = 0

for idx, line in enumerate(lines):
    print(line)
