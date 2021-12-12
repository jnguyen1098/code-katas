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

class Pointer:
    def __init__(self, data=None): self.data = data

class DIR:
    """Directions for graphs/grid problems."""
    NW, N, NE = (-1, -1), (-1,  0), (-1,  1)
    W,     E  = ( 0, -1),           ( 0,  1)
    SW, S, SE = ( 1, -1), ( 1,  0), ( 1,  1)
    DIAG = (NW, NE, SE, SW)
    HORZ = (E, W)
    VERT = (N, S)
    SURR = (*HORZ, *VERT, *DIAG)
    ADJA = (*HORZ, *VERT)

def expect(actual, expected):
    """Compares two values and spits out equality and message."""
    if actual != expected:
        ret_msg = f"FAIL: Expected {expected} but got {actual}"
        ret_sta = False
        return ret_sta, ret_msg
    return True, "PASS"

def get_point(old, new, rows, cols):
    """Translates a point given a displacement tuple."""
    new_x = old[0] + new[0]
    new_y = old[1] + new[1]
    if new_x >= 0 and new_x < rows and new_y >= 0 and new_y < cols:
        return (new_x, new_y)
    return None

def print_arr(arr, sep=""):
    """Array printing but prettier."""
    print('\n'.join([sep.join([str(cell) for cell in row]) for row in arr]))

revdict = lambda dt: {v: k for k, v in dt.items()}

strsep = lambda text, sep=None: list(text.strip().split(sep))
intsep  = lambda text, sep=None: list(map(int, text.strip().split(sep)))
intgrid = lambda text: list(map(int, [char for char in text.strip()]))
parse = lambda pattern, text: re.match(pattern, text).groups()

def yield_line(filename):
    for line in open(filename, "r").read().splitlines():
        yield line
