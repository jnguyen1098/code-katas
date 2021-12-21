#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

from collections import Counter

def roll(pointer):
    result = pointer.data % 100
    pointer.data += 1
    return result

def get_position(curr, advance):
    if (curr + advance) % 10 == 0: return 10
    return (curr + advance) % 10

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(int(line[line.index(":") + 2:]))

    player_1 = lines[0]
    player_2 = lines[1]

    if prob == 1:
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
                player_1 = get_position(player_1, combined)
                score_1 += player_1
            else:
                player_2 = get_position(player_2, combined)
                score_2 += player_2
            player_1s_turn = not player_1s_turn
            rolls += 3
        return losing_score

    if prob == 2:

        pos1 = player_1
        pos2 = player_2
        sco1 = 0
        sco2 = 0
        turn = 1
        win1 = 0
        win2 = 0

        rolls = [3, 4, 5,
                 4, 5, 6,
                 5, 6, 7,
                 4, 5, 6,
                 5, 6, 7,
                 6, 7, 8,
                 5, 6, 7,
                 6, 7, 8,
                 7, 8, 9]
    
        print(rolls)
        roll_freqs = Counter(rolls)
        for outcome, freq in roll_freqs.items():
            print(f"roll  {outcome}     occurs {freq} times")

        print(f"player 1 starts {pos1}")
        print(f"player 2 starts {pos2}")

        limit = 6

        print("player 1 wins", win1, "times")
        print("player 2 wins", win2, "times")

        return 69
