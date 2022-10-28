#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def get_items(data_string):
    assert data_string[-1] == "."

    data_string = data_string.removesuffix(".")
    data_string = data_string.replace(", ", "|")
    items = []

    for statement in data_string.split("|"):
        count, bag_type = parse(r"(\d+) (.+) bags?", statement)
        items.append((count, bag_type))
        
    return items

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        if line == "":
            break
        lines.append(parse(r"(.+) bags contain (?:(no other bags\.)|(?:(\d+.+[\.,])+))", line))

    pprint(lines)

    bags = []

    for bag_name, empty_group, data_group in lines:
        if empty_group is None:
            assert data_group is not None
            bags.append((bag_name, get_items(data_group)))
        if data_group is None:
            assert empty_group == "no other bags."
            bags.append((bag_name, []))

    pprint(bags)

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
