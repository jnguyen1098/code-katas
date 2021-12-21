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


    class Game:
        def __init__(self, player_1_start, player_2_start):
            self.pos1 = player_1_start
            self.pos2 = player_2_start

            self.sco1 = 0
            self.sco2 = 0

            self.turn = 1

            self.win1 = 0
            self.win2 = 0

            rolls = [3, 4, 5,
                     4, 5, 6,
                     5, 6, 7,
                     4, 5, 6,
                     5, 6, 7,
                     6, 7, 8,
                     5, 6, 7,
                     6, 7, 8,
                     7, 8, 9]

            self.roll_freqs = Counter(rolls)
            for outcome, freq in self.roll_freqs.items():
                print(f"roll  {outcome}     occurs {freq} times")

            print(f"player 1 starts {self.pos1}")
            print(f"player 2 starts {self.pos2}")

    game = Game(player_1, player_2)

    if prob == 1:
        return losing_score
    elif prob == 2:
        """
        return p1_wins if p1_wins > p2_wins else p2_wins
        """
        return -1
    else:
        print("Invalid problem code")
        exit()
