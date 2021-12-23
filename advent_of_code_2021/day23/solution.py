#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

"""
4 sides
4 intersections
3 betweeners
8 resting spots = [4 columns] x [2 rows]

there are 7 resting spots. 4 intersections can't be rested at

Will never stop on any hole, so [h1,h2,h3,h4]
Will only go into a room if it is theirs
Will only go into a room if no incorrect amphipods are there
 (in other words, an amphipod can only be in an incorrect room
  if it was spawned in such. the second it leaves, it can't go back)
Amphipods that move to the hallway can't be intermediate-adjusted;
  aka, once they stop in the hallway, they stay frozen until they can
  move into a room

#############
#           #
###B#C#B#D###
  #A#D#C#A#
  #########
"""

def solve(prob, inputname):

    rooms = []

    if inputname == "example":
        rooms = [
            ["B", "A"],
            ["C", "D"],
            ["B", "C"],
            ["D", "A"],
        ]
    else:
        print("unknown input")
        exit()

    energy = 0

    if prob == 1:
        return energy
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()
