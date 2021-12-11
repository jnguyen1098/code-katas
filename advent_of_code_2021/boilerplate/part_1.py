#!/usr/bin/env python3

import copy
import sys
import math
import re

sys.path.append("..")

from math import ceil, floor, inf, log, sqrt
from collections import defaultdict, deque

# EFFECTS: (bold|dim|undr|blnk|rev|hidn)
# COLOURS: (l|b)?(red|grn|yel|blu|mag|cya|wht)
from ansi import *

MOD = 1000000007

def print_arr(arr, sep=""):
    print('\n'.join([sep.join([str(cell) for cell in row]) for row in arr]))

revdict = lambda dt: {v: k for k, v in dt.items()}

introw = lambda text: list(map(int, text.strip().split()))
intgrid = lambda text: list(map(int, [char for char in text.strip()]))
parse = lambda pattern, text: re.match(pattern, text).groups()

def yield_line(filename):
    for line in open(filename, "r").read().splitlines():
        yield line

if __name__ == "__main__":
    inputname = "real"
    inputname = "example"
    inputname = "small"

    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(line)

    print_arr(lines)

    print(f"{len(lines)} lines in the array")
