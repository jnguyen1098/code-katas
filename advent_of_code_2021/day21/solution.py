#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

from collections import Counter

ONE, TWO = (0, 1)

def get_next_position(curr, advance):
    return (curr + advance - 1) % 10 + 1

def encode(pos1, sco1, pos2, sco2, turn):
    return f"{pos1},{sco1}|{pos2},{sco2}|{turn}"
    return f"{pos1},{sco1 if sco1 < 10 else 'W'}|{pos2},{sco2 if sco2 < 10 else 'W'}|{turn}"

def decode(serialized):
    spl = serialized.split("|")
    p1 = spl[0].split(",")
    p2 = spl[1].split(",")
    turn = spl[2]
    return int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), int(turn)

def normal_game(player_1, player_2):
    position_of_player = [player_1, player_2]
    score_of_player = [0, 0]
    curr_die_val = 0
    rolls = 0
    curr_player = 0

    while score_of_player[ONE] < 1000 and score_of_player[TWO] < 1000:

        next_roll = (3 * curr_die_val) + 6  # (die + 1) + (die + 2) + (die + 3)  ;-)
        position_of_player[curr_player] = get_next_position(position_of_player[curr_player], next_roll)
        score_of_player[curr_player] += position_of_player[curr_player]

        curr_player = ~curr_player
        curr_die_val += 3
        rolls += 3

    return rolls * min(score_of_player)

def solve(prob, inputname):

    player_1, player_2 = [int(line[line.index(":") + 2:]) for line in yield_line(inputname)]

    if prob == 1: return normal_game(player_1, player_2)

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
    
        tree = {}

        def get_wins(state, level):
            if memo := tree.get(state):
                return memo
            p1, s1, p2, s2, turn = decode(state)
            p1_wins = 0
            p2_wins = 0
            for roll in rolls:
                if turn == 1:
                    new_p1 = get_next_position(p1, roll)
                    new_s1 = s1 + new_p1
                    new_state = encode(new_p1, new_s1, p2, s2, 2)
                    if new_s1 >= 21:
                        p1_wins += 1
                    else:
                        incr1, incr2 = get_wins(new_state, level + 1)
                        p1_wins += incr1
                        p2_wins += incr2
                elif turn == 2:
                    new_p2 = get_next_position(p2, roll)
                    new_s2 = s2 + new_p2
                    new_state = encode(p1, s1, new_p2, new_s2, 1)
                    if new_s2 >= 21:
                        p2_wins += 1
                    else:
                        incr1, incr2 = get_wins(new_state, level + 1)
                        p1_wins += incr1
                        p2_wins += incr2
            tree[state] = (p1_wins, p2_wins)
            return tree[state]

        p1_wins, p2_wins = get_wins(f"{player_1},0|{player_2},0|1", level=1)
        print(f"Player 1 won {p1_wins} times")
        print(f"Player 2 won {p2_wins} times")

        return max(p1_wins, p2_wins)
