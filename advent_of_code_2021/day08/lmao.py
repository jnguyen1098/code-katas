#!/usr/bin/env python3

import sys
import math

from math import gcd, floor, sqrt, log
from collections import defaultdict, deque
from bisect import bisect_left, bisect_right

MOD = 1000000007

inputname = "real"
inputname = "example"
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

lines = open(inputname, "r").read().splitlines()

import itertools

def attempt(bf, signals, result):
    signals = " ".join(["".join(sorted(word)) for word in signals.split()])
    result = " ".join(["".join(sorted(word)) for word in result.split()])
    signals = list(signals)
    result = list(result)
    for i in range(len(signals)):
        if signals[i] == " ": continue
        signals[i] = bf[signals[i]]
    for i in range(len(result)):
        if result[i] == " ": continue
        result[i] = bf[result[i]]
    signals = "".join(signals)
    result = "".join(result)
    print(signals, "    ", result)
    for signal in signals.split():
        if signal not in digit:
            return False
    return True

found = False

def go(signals, result):
    for perm in itertools.permutations("abcdefg"):
        bf = {a: b for a, b in zip(perm, "abcdefg")}
        if not attempt(bf, signals, result):
            continue
        else:
            print("found")
            print(bf)
            exit()

for line in lines:
    left, right = line.split(" | ")
    go(left, right)

exit()

def deduce(letters, translate):
    if len(letters) == 2:
        return 1
    if len(letters) == 3:
        return 7
    if len(letters) == 4:
        return 4
    if len(letters) == 5:
        if translate["b"] in letters:
            return 5
        if translate["e"] in letters:
            return 2
        return 3
    if len(letters) == 6:
        if translate["d"] not in letters:
            return 0
        if translate["c"] in letters:
            return 9
        return 6
    if len(letters) == 7:
        return 8

def fix_dictionary(translate, extra, fives, sixes):
    extra_rev = {v: k for k, v in extra.items()}
    """
    print("map", translate)
    print("mapkeys", translate)
    print("extra", extra)
    print("extra_rev", extra_rev)
    print("fives", fives)
    print("sixes", sixes)
    """
    for key, value in extra_rev.items():
        for i in range(len(value)):
            if letters[key][i] not in translate:
                translate[letters[key][i]] = value[i]
            elif translate[letters[key][i]] != value[i]:
                translate[letters[key][i]] = value[i]
    lts = set(["a", "b", "c", "d", "e", "f", "g"])
    rts = set(["a", "b", "c", "d", "e", "f", "g"])
    for key, value in translate.items():
        lts.remove(key)
        rts.remove(key)
    try:
        translate[lts.pop()] = rts.pop()
    except:
        pass


count = 0

for line in lines:
    print(line)

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
    lmao = []
    for word in result:
        broken = list(word)
        for i in range(len(broken)):
            broken[i] = translate.get(broken[i], "?")
        result = "".join(broken)
        res = deduce(result, translate)
        lmao.append(str(res))
        if res in [1, 4, 7, 8]:
            count += 1
    fuck = int("".join(lmao))
    print(fuck)
    #print(translate)

print(count)
