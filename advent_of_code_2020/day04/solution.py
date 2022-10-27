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

def valid_passport_soft(passport):
    FIELDS = set([
        "byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid",
    ])
    diff = (FIELDS - passport.keys()) 
    return len(diff) == 0 or diff == set(["cid"])

def height_valid(height):
    if not height or (not height.endswith("cm") and not height.endswith("in")):
        return False
    if height.endswith("cm"):
        return 150 <= int(height.removesuffix("cm")) <= 193
    if height.endswith("in"):
        return 59 <= int(height.removesuffix("in")) <= 76
    return True

def hair_colour_valid(colour):
    if colour == "" or not colour:
        return False
    if colour[0] != "#":
        return False
    if len(colour) != 7:
        return False
    for i in range(1, len(colour)):
        if colour[i] not in "0123456789" and colour[i] not in "abcdef":
            return False
    return True

def eye_colour_valid(colour):
    return colour in set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])

def passport_id_valid(passport_id):
    if len(passport_id) != 9:
        return False
    for i in range(len(passport_id)):
        if passport_id[i] not in "0123456789":
            return False
    return True

def valid_passport_hard(passport):
    if not valid_passport_soft(passport):
        return False

    if not 1920 <= int(passport["byr"]) <= 2002:
        return False

    if not 2010 <= int(passport["iyr"]) <= 2020:
        return False

    if not 2020 <= int(passport["eyr"]) <= 2030:
        return False

    if not height_valid(passport["hgt"]):
        return False

    if not hair_colour_valid(passport["hcl"]):
        return False

    if not eye_colour_valid(passport["ecl"]):
        return False

    if not passport_id_valid(passport["pid"]):
        return False

    return True

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(line)

    passports = get_passports(lines)

    if prob == 1:
        valid_count = 0

        for passport in passports:
            if valid_passport_soft(passport):
                valid_count += 1

        return valid_count
    elif prob == 2:
        valid_count = 0

        for passport in passports:
            if valid_passport_hard(passport):
                valid_count += 1

        return valid_count
    else:
        print("Invalid problem code")
        exit()
