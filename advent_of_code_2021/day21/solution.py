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

def encode(pos1, sco1, pos2, sco2, turn):
    return f"{pos1},{sco1}|{pos2},{sco2}|{turn}"
    return f"{pos1},{sco1 if sco1 < 10 else 'W'}|{pos2},{sco2 if sco2 < 10 else 'W'}|{turn}"

def decode(serialized):
    spl = serialized.split("|")
    p1 = spl[0].split(",")
    p2 = spl[1].split(",")
    turn = spl[2]
    return int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), int(turn)

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
    
        """
        print(rolls)
        roll_freqs = Counter(rolls)
        for outcome, freq in roll_freqs.items():
            print(f"roll  {outcome}     occurs {freq} times")

        print(f"player 1 starts {pos1}")
        print(f"player 2 starts {pos2}")

        limit = 6

        print("player 1 wins", win1, "times")
        print("player 2 wins", win2, "times")
        """

        """
        Roll 1, then 2, then 3
        When score is >= 10, player wins
        """
        tree = {}

        def print_state(state):
            position_1, score_1, position_2, score_2, turn = decode(state)
            #print(f"{state} is {position_1=}  {score_1=}  {position_2=}  {score_2=}  {turn=}")
            print(state)

        def indent(level):
            return " " * 4 * level

        print()
        def get_wins(state, level):
            """
            print(indent(level - 1), end="")
            print_state(state)
            """
            if memo := tree.get(state):
                """
                print(f"{indent(level)} This position was memoized. Returning {memo=}")
                """
                return memo
            p1, s1, p2, s2, turn = decode(state)
            p1_wins = 0
            p2_wins = 0
            """
            for roll in [1, 2, 3]:
            """
            for roll in rolls:
                if turn == 1:
                    new_p1 = get_position(p1, roll)
                    new_s1 = s1 + new_p1
                    new_state = encode(new_p1, new_s1, p2, s2, 2)
                    """
                    print(f"{indent(level)}P1 rolled {roll}. Pos {p1} -> {new_p1}. Score {s1} -> {new_s1}")
                    print(f"{indent(level + 1)}New state is {new_state}")
                    """
                    if new_s1 >= 21:
                        """
                        print(f"{indent(level + 2)}Because p1 has score {new_s1}, they win this node")
                        """
                        p1_wins += 1
                    else:
                        """
                        print(f"{indent(level + 2)}Nobody wins yet. Recursive request for {new_state}\n")
                        """
                        incr1, incr2 = get_wins(new_state, level + 1)
                        p1_wins += incr1
                        p2_wins += incr2
                elif turn == 2:
                    new_p2 = get_position(p2, roll)
                    new_s2 = s2 + new_p2
                    new_state = encode(p1, s1, new_p2, new_s2, 1)
                    """
                    print(f"{indent(level)}P2 rolled {roll}. Pos {p2} -> {new_p2}. Score {s2} -> {new_s2}")
                    print(f"{indent(level + 1)}New state is {new_state}")
                    """
                    if new_s2 >= 21:
                        """
                        print(f"{indent(level + 2)}Because p2 has score {new_s2}, they win this node")
                        """
                        p2_wins += 1
                    else:
                        """
                        print(f"{indent(level + 3)}Nobody wins yet. Recursive request for {new_state}\n")
                        """
                        incr1, incr2 = get_wins(new_state, level + 1)
                        p1_wins += incr1
                        p2_wins += incr2
                else:
                    print("Impossible turn", turn)
                    exit(1)
                """
                print()
                """
            tree[state] = (p1_wins, p2_wins)
            return tree[state]

        p1_wins, p2_wins = get_wins("10,0|8,0|1", level=1)
        print(f"Player 1 won {p1_wins} times")
        print(f"Player 2 won {p2_wins} times")

        return 69
