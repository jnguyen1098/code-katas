#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def roll(pointer):
    result = pointer.data % 100
    pointer.data += 1
    return result

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(int(line[line.index(":") + 2:]))

    player_1 = lines[0]
    player_2 = lines[1]

    score_1 = 0
    score_2 = 0

    pointer = Pointer(1)

    rolls = 0
    player_1s_turn = True
    while True:
        res1 = roll(pointer)
        res2 = roll(pointer)
        res3 = roll(pointer)
        combined = res1 + res2 + res3
        if score_1 >= 1000:
            losing_score = score_2 * rolls
            break
        elif score_2 >= 1000:
            losing_score = score_1 * rolls
            break
        elif player_1s_turn:
            if (player_1 + combined) % 10 == 0:
                player_1 = 10
            else:
                player_1 = ((player_1 + combined) % 10)
            score_1 += player_1
        else:
            if (player_2 + combined) % 10 == 0:
                player_2 = 10
            else:
                player_2 = ((player_2 + combined) % 10)
            score_2 += player_2
        player_1s_turn = not player_1s_turn
        rolls += 3

    dominant_wins = 0

    if prob == 1:
        return losing_score
    elif prob == 2:
        return dominant_wins
    else:
        print("Invalid problem code")
        exit()
