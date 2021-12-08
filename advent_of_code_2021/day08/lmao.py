#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

MOD = 1000000007

inputname = "example"
inputname = "real"
inputname = "small"

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

def deduce(letters, translate):
    if len(letters) == 2:
        return 1
    if len(letters) == 3:
        return 7
    if len(letters) == 4:
        return 4
    if len(letters) == 5:
        if "b" in letters:
            return 5
        if "e" in letters:
            return 2
        return 3
    if len(letters) == 6:
        if "d" not in letters:
            return 0
        if "c" in letters:
            return 9
        return 6
    if len(letters) == 7:
        return 8

def fix_dictionary(translate, extra, fives, sixes):
    extra_rev = {v: k for k, v in extra.items()}
    print("map", translate)
    print("mapkeys", translate)
    print("extra", extra)
    print("extra_rev", extra_rev)
    print("fives", fives)
    print("sixes", sixes)
    for key, value in extra_rev.items():
        print(letters[key], value)
        for i in range(len(value)):
            if letters[key][i] not in translate:
                print(f"{letters[key][i]} not in translate")
                translate[letters[key][i]] = value[i]
            elif translate[letters[key][i]] != value[i]:
                print("redefined")
                translate[letters[key][i]] = value[i]
    lts = set(["a", "b", "c", "d", "e", "f", "g"])
    rts = set(["a", "b", "c", "d", "e", "f", "g"])
    for key, value in translate.items():
        lts.remove(key)
        rts.remove(key)
    translate[lts.pop()] = rts.pop()

lines = open(inputname, "r").read().splitlines()

count = 0

for line in lines:
    translate = {}
    extra = {}
    fives = []
    sixes = []
    left, right = line.split(" | ")
    signals = ["".join(sorted(word)) for word in left.split()]
    signals = [word for word in left.split()]
    result = ["".join(sorted(word)) for word in right.split()]
    result = [word for word in right.split()]

    for signal in signals:
        if len(signal) == 2:
            translate[signal[0]] = "c"
            translate[signal[1]] = "f"
            extra[signal] = 1
        elif len(signal) == 3:
            translate[signal[0]] = "a"
            translate[signal[1]] = "c"
            translate[signal[2]] = "f"
            extra[signal] = 7
        elif len(signal) == 4:
            translate[signal[0]] = "b"
            translate[signal[1]] = "c"
            translate[signal[2]] = "d"
            translate[signal[3]] = "f"
            extra[signal] = 4
        elif len(signal) == 5:
            fives.append("".join(sorted(signal)))
        elif len(signal) == 6:
            sixes.append("".join(sorted(signal)))
    fix_dictionary(translate, extra, fives, sixes)
    for word in result:
        broken = list(word)
        for i in range(len(broken)):
            broken[i] = translate.get(broken[i], "?")
        result = "".join(broken)
        res = deduce(result, translate)
        if res in [1, 4, 7, 8]:
            count += 1
    print(translate)


print(count)
