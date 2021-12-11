#!/usr/bin/env python3

import copy
import sys
import math

sys.path.append("..")

from math import ceil, floor, inf, log, sqrt
from collections import defaultdict, deque

# EFFECTS: (bold|dim|undr|blnk|rev|hidn)
# COLOURS: (l|b)?(red|grn|yel|blu|mag|cya|wht)
from ansi import *

MOD = 1000000007

def rev_dict(input_dict):
    return {v: k for k, v in input_dict.items()}

def print_arr(arr):
    print('\n'.join([' '.join([str(cell) for cell in row]) for row in arr]))

introw = lambda text: list(map(int, text.strip().split()))
intgrid = lambda text: list(map(int, [char for char in text.strip()]))

inputname = "real"
inputname = "example"

lines = open(inputname, "r").read().splitlines()

for idx, line in enumerate(lines):
    print(idx, line)
print("linecount:", len(lines))
