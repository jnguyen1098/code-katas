#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def split_lines_into_key_value_pairs(lines):
    kv = []

    for line in lines:
        if line.strip() == "":
            continue
        for token in (tokens := line.split(" ")):
            key, value = token.split(":")
            kv.append((key, value))

    return kv

def get_passports(raw_lines):
    return []

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(line)

    passports = get_passports(lines)

    print_arr(passports)

    print(f"{len(lines)} in the array")

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
