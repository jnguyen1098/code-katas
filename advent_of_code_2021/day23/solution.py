#!/usr/bin/env python3

import itertools
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
#ss s s s ss#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

LEFT, MIDDLE, RIGHT = 0, 1, 2
L1, L2, M1, M2, M3, R1, R2 = 3, 4, 5, 6, 7, 8, 9

class Game:
    def __init__(self, cols):
        self.cols = cols
        self.tops = {
            L1: None, L2: None,
            M1: None, M2: None, M3: None,
            R1: None, R2: None,
        }

    def jump_up(self, col, target):
        val = self.cols[col].pop()
        assert group in [LEFT, MIDDLE, RIGHT]
        assert target in [L1, L2, M1, M2, M3, R1, R2]
        self.tops[target] = val

    def __str__(self):
        cols = list(itertools.zip_longest(*self.cols, fillvalue=" "))
        lines = [
            "#############",
            f"#{self.tops[L1] or ' '}{self.tops[L1] or ' '} {self.tops[M1] or ' '} {self.tops[M2] or ' '} {self.tops[M3] or ' '} {self.tops[R1] or ' '}{self.tops[R2] or ' '}#",
        ]
        for idx, col in enumerate(reversed(cols)):
            if idx == 0: lines.append(f"###{col[0]}#{col[1]}#{col[2]}#{col[3]}###")
            else: lines.append(f"  #{col[0]}#{col[1]}#{col[2]}#{col[3]}#  ")
        lines.append("  #########  ")
        return "\n".join(lines)
        

def solve(prob, inputname):

    if inputname == "example":
        game = Game([
            ["A", "B"],
            ["D", "C"],
            ["C", "B"],
            ["A", "D"],
        ])
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
