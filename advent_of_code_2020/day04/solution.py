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

def create_passport(pairs):
    passport = {}

    for key, value in pairs:
        assert key not in passport
        passport[key] = value

    return passport

def get_passports(raw_lines):
    passports = []

    assert raw_lines and raw_lines[0] != ""

    curr_passport_lines = []

    for line in raw_lines:
        if line != "":
            curr_passport_lines.append(line)
            continue
        kv_pairs = split_lines_into_key_value_pairs(curr_passport_lines)
        passport = create_passport(kv_pairs)
        passports.append(passport)
        curr_passport_lines.clear()

    return passports

def valid_passport(passport):
    FIELDS = set([
        "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid",
    ])
    diff = (FIELDS - passport.keys()) 
    return len(diff) == 0 or diff == set(["cid"])

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(line)

    passports = get_passports(lines)

    print(f"{len(lines)} in the array")

    if prob == 1:
        valid_count = 0

        for passport in passports:
            if valid_passport(passport):
                valid_count += 1

        return valid_count
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
