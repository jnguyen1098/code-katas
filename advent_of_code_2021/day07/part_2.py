#!/usr/bin/env python3

import sys
import math

tmp_data = [int(tmp) for tmp in open("input", "r").read().split(",")]

def sum_of_n(n):
    s = 0
    for i in range(1, n + 1):
        s += i
    return s

def get_triangle(n):
    return (n * (n + 1)) // 2

strategy = get_triangle

def move_all_to(crabs, num):
    cost = 0
    for i in range(len(crabs)):
        cost += strategy(abs(crabs[i] - num))
    return cost

min_cost = math.inf

for i in range(len(tmp_data)):
    min_cost = min(min_cost, move_all_to(tmp_data, i))

print(min_cost)


