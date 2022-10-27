#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(parse(r"(\d+)-(\d+) ([a-z]): (.+)", line))

    if prob == 1:
        count = 0

        def satisfies(password, char, lo, hi):
            counter = Counter(password)
            return lo <= counter[char] <= hi

        for lo, hi, char, password in lines:
            if satisfies(password, char, int(lo), int(hi)):
                count += 1

        return count
    elif prob == 2:
        count = 0

        def satisfies(password, char, lo, hi):
            return (password[lo - 1] == char) ^ (password[hi - 1] == char)

        for lo, hi, char, password in lines:
            if satisfies(password, char, int(lo), int(hi)):
                count += 1

        return count
    else:
        print("Invalid problem code")
        exit()
