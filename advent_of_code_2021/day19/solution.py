#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def solve(prob, inputname):

    scanners = []
    scanner = []

    for line in yield_line(inputname):
        if line.startswith("---"):
            continue
        elif line == "":
            if scanner:
                scanners.append(scanner[:])
            scanner.clear()
        else:
            scanner += [int(thing) for thing in line.split(",")]

    for scanner in scanners:
        print(scanner)

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
