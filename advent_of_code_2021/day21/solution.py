#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

from collections import Counter

ONE, TWO = (0, 1)
ROLL_DISTRIBUTION = {3: 1,  4: 3,  5: 6,  6: 7,  7: 6,  8: 3,  9: 1}

def get_next_position(curr, advance):
    return (curr + advance - 1) % 10 + 1

def encode(pos1, pos2, sco1, sco2, turn):
    return f"{pos1},{pos2}|{sco1},{sco2}|{turn}"

def decode(serialized):
    spl = serialized.split("|")
    pos = spl[0].split(",")
    sco = spl[1].split(",")
    turn = spl[2]
    return int(pos[ONE]), int(pos[TWO]), int(sco[ONE]), int(sco[TWO]), int(turn)

def get_losing_score(player_1, player_2):
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

"""
DFS algorithm that uses backtracking and top-down DP/memoization.

Explores the game tree until it reaches a game over, then increments the respective winner.

Game is won when there is a score of 21 or over.
"""
def get_universes(state, win_cache={}):

    if memo := win_cache.get(state):
        return memo

    curr_player = 1
    win_count_for_player = [0, 0]

    data = decode(state)
    position_of_player, score_of_player, current_player = data[0:2], data[2:4], data[4]

    for roll, freq in ROLL_DISTRIBUTION.items():
        new_pos = get_next_position(position_of_player[current_player], roll)
        new_sco = score_of_player[current_player] + new_pos
        if new_sco >= 21:
            win_count_for_player[current_player] += freq
        else:
            if current_player == ONE:
                incr1, incr2 = get_universes(encode(new_pos, position_of_player[TWO], new_sco, score_of_player[TWO], TWO))
            elif current_player == TWO:
                incr1, incr2 = get_universes(encode(position_of_player[ONE], new_pos, score_of_player[ONE], new_sco, ONE))
            win_count_for_player[ONE] += incr1 * freq
            win_count_for_player[TWO] += incr2 * freq

    win_cache[state] = win_count_for_player
    return win_cache[state]

def solve(prob, inputname):

    position_for_player = [int(line[line.index(":") + 2:]) for line in yield_line(inputname)]

    if prob == 1:
        return get_losing_score(position_for_player[ONE], position_for_player[TWO])
    if prob == 2:
        return max(get_universes(f"{position_for_player[ONE]},{position_for_player[TWO]}|0,0|{ONE}", {}))
