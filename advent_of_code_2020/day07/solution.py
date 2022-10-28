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

    bags = {}

    for bag_name, empty_group, data_group in lines:
        if empty_group is None:
            assert data_group is not None
            assert bag_name not in bags
            bags[bag_name] = get_items(data_group)
        if data_group is None:
            assert empty_group == "no other bags."
            assert bag_name not in bags
            bags[bag_name] = []

    def flatten_contents(target_bag_name: str) -> set[str]:

        if bags[target_bag_name] == []:
            return set([target_bag_name])

        answer = set([target_bag_name])

        for child_count, child_bag_type in bags[target_bag_name]:
            answer.add(child_bag_type)
            for sub_child in flatten_contents(child_bag_type):
                answer.add(sub_child)

        return answer

    if prob == 1:
        count = 0
        for bag_name in bags.keys():
            if bag_name == "shiny gold":
                continue
            if "shiny gold" in flatten_contents(bag_name):
                count += 1
        return count
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
