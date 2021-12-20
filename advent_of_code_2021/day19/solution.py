#!/usr/bin/env python3

import json
import sys
sys.path.append("..")

from ansi import *
from comp import *

def permute(a, b, c):
	yield (+a, +b, +c)
	yield (+b, +c, +a)
	yield (+c, +a, +b)
	yield (+c, +b, -a)
	yield (+b, +a, -c)
	yield (+a, +c, -b)

	yield (+a, -b, -c)
	yield (+b, -c, -a)
	yield (+c, -a, -b)
	yield (+c, -b, +a)
	yield (+b, -a, +c)
	yield (+a, -c, +b)

	yield (-a, +b, -c)
	yield (-b, +c, -a)
	yield (-c, +a, -b)
	yield (-c, +b, +a)
	yield (-b, +a, +c)
	yield (-a, +c, +b)

	yield (-a, -b, +c)
	yield (-b, -c, +a)
	yield (-c, -a, +b)
	yield (-c, -b, -a)
	yield (-b, -a, -c)
	yield (-a, -c, -b)

def transform(list_of_beacons):
    new_list = []
    for i in range(24):
        new_list.append([])

    for beacon in list_of_beacons:
        for jdx, transform in enumerate(permute(beacon[0], beacon[1], beacon[2])):
            new_list[jdx].append(transform)

    return new_list

def get_intersection(scanner1, scanner2):
    set1 = set(json.dumps(thing) for thing in scanner1)
    set2 = set(json.dumps(thing) for thing in scanner2)
    return set1 & set2

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
            scanner.append([int(thing) for thing in line.split(",")])

    beacon_count = 0

    for i in range(len(scanners)):
        transformations = transform(scanners[i])

    if prob == 1:
        return beacon_count
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
