#!/usr/bin/env python3.11
"""Implementation for Advent of Code 2022, Day 16 with BnB."""

from __future__ import annotations

import itertools
import re
from functools import cached_property
from typing import Iterable

INF = 0x3F3F3F3F

State = tuple[int, int, int]  # curr_flow, turns_left, curr_relief
CURR_FLOW, TURNS_LEFT, CURR_RELIEF = 0, 1, 2

Valve = tuple[str, int, list[str]]  # name, flow, exits
NAME, FLOW, EXITS = 0, 1, 2

Result = tuple[int, list[str], int]  # payout, path, turns_left

# (a - y) * 26 + (b - y)
# 26a - 26y + b - y
# 26a - 27y + b
def valve_to_num(valve: str) -> int:
    return 26 * ord(valve[0]) + ord(valve[1]) - 1755

def num_to_valve(val: int) -> str:
    res = ["A", "A"]

    if val < 26:
        res[1] = chr(65 + val)
    else:
        res[0] = chr(65 + (val // 26) % 26)
        res[1] = chr(65 + (val % 26))

    return "".join(res)

class TravellingPlumber:
    """Represents a branch-and-bound implementation of AOC 2022, Day 16: Proboscidea Volcanium."""

    def __init__(self, valves: list[Valve], max_turns: int, start_valve_name: str) -> None:
        self.valves = valves
        self.max_turns = max_turns
        self.start_valve_name = start_valve_name

    @cached_property
    def valve_by_name(self) -> dict[str, Valve]:
        """Takes the valve list and creates a dictionary for easy reference."""
        valve_by_name = {}
        for valve in self.valves:
            valve_by_name[valve[NAME]] = valve
        return valve_by_name

    @cached_property
    def cost_between(self) -> dict[str, dict[str, int]]:
        """Establishes the transitive closure of the graph using the Floyd-Warshall algorithm."""
        cost_between = {}

        for valve in self.valve_by_name.values():
            for exit_name in valve[EXITS]:
                cost_between[valve[NAME], exit_name] = 1

        for k in (valve_names := list(self.valve_by_name.keys())):
            for i in valve_names:
                for j in valve_names:
                    if i == j:
                        continue
                    cost_between[i, j] = min(
                        cost_between.get((i, j), INF),
                        cost_between.get((i, k), INF) + cost_between.get((k, j), INF),
                    )

        expanded_dict: dict[str, dict[str, int]] = {}

        for pair, cost in cost_between.items():
            left, right = pair
            rev_cost = cost_between[right, left]
            assert cost == rev_cost, f"Cost-between-valves is not symmetric between {pair} and {right, left}"
            if left not in expanded_dict:
                expanded_dict[left] = {}
            if right not in expanded_dict:
                expanded_dict[right] = {}
            expanded_dict[left][right] = cost
            expanded_dict[right][left] = cost

        return expanded_dict

    @cached_property
    def canonical_graph(self) -> dict[str, dict[str, int]]:
        """
        Takes the transitive closure created by the Floyd-Warshall algorithm and reduces it.

        Now that every shortest cost is found, we only want non-zero interactions.
        """
        canonical_graph: dict[str, dict[str, int]] = {}

        for quiescent_valve_name in self.quiescent_valves:
            if quiescent_valve_name not in canonical_graph:
                canonical_graph[quiescent_valve_name] = {}
            for target in self.cost_between[quiescent_valve_name]:
                if target not in self.quiescent_valves:
                    continue
                if target not in canonical_graph:
                    canonical_graph[target] = {}
                canonical_graph[quiescent_valve_name][target] = self.cost_between[quiescent_valve_name][target]
                canonical_graph[target][quiescent_valve_name] = self.cost_between[target][quiescent_valve_name]

        canonical_graph[self.start_valve_name] = {}
        for end in self.cost_between[self.start_valve_name]:
            if end not in self.quiescent_valves:
                continue
            canonical_graph[self.start_valve_name][end] = self.cost_between[self.start_valve_name][end]

        return canonical_graph

    @cached_property
    def maximal_valve_ordering(self) -> list[str]:
        """The ordering of valves based on flow."""
        return sorted(
            self.quiescent_valves,
            key=lambda valve_name: self.valve_by_name[valve_name][FLOW],
            reverse=True,
        )

    @cached_property
    def quiescent_valves(self) -> set[str]:
        """Valves that have non-zero flow."""
        return {valve[NAME] for valve in self.valves if valve[FLOW] > 0 and valve[NAME] != self.start_valve_name}

    @staticmethod
    def from_filename(*, path: str, start_valve: str, max_turns: int) -> "TravellingPlumber":
        """Parses the valves for the problem from a file."""
        with open(path, "r", encoding="ascii") as file_object:
            lines = [line.rstrip("\n") for line in file_object]
        valves = []
        for line in lines:
            parse = re.findall(r"([A-Z]{2}|\d+)", line)
            name, flow, exits = parse[0], int(parse[1]), parse[2:]
            valves.append((name, flow, exits))
        return TravellingPlumber(valves=valves, start_valve_name=start_valve, max_turns=max_turns)


    def solve(self, ignore_set: set[str] | frozenset[str] = frozenset()) -> Result:
        """
        Solves Advent of Code, 2022, Day 16 for a single agent.

        Pre-processes the valves, a canonical graph, and maximal ordering, all of which rely on
        the maximum turns, start valve, and the valves themselves.
        """

        def get_payout(state: State) -> int:
            return state[CURR_RELIEF] + state[CURR_FLOW] * state[TURNS_LEFT]

        start_node = (0, self.max_turns, 0)

        best_payout = get_payout(start_node)
        best_relief_accum = [-1] * self.max_turns
        best_valve_path = []
        best_turns_left = INF

        curr_valve_path = [self.start_valve_name]
        curr_relief_accum = [-1] * self.max_turns
        curr_valve_set = set() | ignore_set

        def explore_node(curr_node: State) -> None:

            nonlocal best_payout
            nonlocal best_relief_accum
            nonlocal best_valve_path
            nonlocal best_turns_left

            curr_valve = curr_valve_path[-1]
            curr_relief = curr_node[CURR_RELIEF]

            if (curr_payout := get_payout(curr_node)) > best_payout:
                best_payout = curr_payout
                best_relief_accum = curr_relief_accum[:]
                best_valve_path = curr_valve_path[:]
                best_turns_left = curr_node[TURNS_LEFT]

            if curr_node[TURNS_LEFT] == 1:
                return

            for next_valve_name in self.maximal_valve_ordering:
                if next_valve_name in curr_valve_set:
                    continue
                activation_cost_in_turns = self.canonical_graph[curr_valve][next_valve_name] + 1
                next_turns_left = curr_node[TURNS_LEFT] - activation_cost_in_turns
                if curr_node[TURNS_LEFT] - activation_cost_in_turns < 1:
                    continue
                next_relief = curr_relief + (curr_node[CURR_FLOW] * activation_cost_in_turns)
                next_flow = curr_node[CURR_FLOW] + self.valve_by_name[next_valve_name][FLOW]
                next_state = (
                    next_flow,
                    next_turns_left,
                    next_relief,
                )
                if best_relief_accum[self.max_turns - next_turns_left] >= next_relief:
                    continue
                curr_valve_set.add(next_valve_name)
                curr_valve_path.append(next_valve_name)
                curr_relief_accum[self.max_turns - next_turns_left] = next_relief
                explore_node(next_state)
                curr_valve_path.pop()
                curr_valve_set.remove(next_valve_name)

        explore_node(start_node)
        return best_payout, best_valve_path, best_turns_left


class ElephantSolver:
    """Container class for solving AOC 2022, Day 16."""

    def __init__(self, plumber: TravellingPlumber) -> None:
        """Instantiates the Elephant Solver."""
        self.plumber = plumber

    @cached_property
    def sorted_quiescent_valves(self) -> list[str]:
        """Takes our quiescent valves and creates a sorted view."""
        return sorted(self.plumber.quiescent_valves)

    def get_subset_from_mask(self, mask: list[int]) -> frozenset[str]:
        """Takes a given bitmask and returns a set of valves based on membership."""
        return frozenset(itertools.compress(self.sorted_quiescent_valves, mask))

    @staticmethod
    def get_nth_mask(idx: int, cardinality: int) -> list[int]:
        """Gets a particular bitmask based on position within cardinality."""
        return list(map(int, bin(2**cardinality + idx)[3:]))

    def set_to_mask(self, valve_set: set[str]) -> list[int]:
        """Takes a set of valves and converts it back to a bitmask."""
        mask = []
        for valve in self.sorted_quiescent_valves:
            if valve in valve_set:
                mask.append(1)
            else:
                mask.append(0)
        return mask

    @staticmethod
    def mask_to_num(mask: list[int]) -> int:
        """Takes a given bitmask and converts it back to an integer."""
        return int("".join(map(str, mask)), 2)

    def generate_all_subsets_starting_from(self, start_idx: int = 0) -> Iterable[frozenset[str]]:
        """Iterates all subsets modulo the given cardinality, starting at a certain position within."""
        for i in range(2 ** len(self.plumber.quiescent_valves)):
            final_value = (i + start_idx) % (2 ** len(self.plumber.quiescent_valves))
            mask = self.get_nth_mask(final_value, len(self.plumber.quiescent_valves))
            subset = self.get_subset_from_mask(mask)
            yield subset

    def get_single_agent_result(self, ignore_set: frozenset[str] = frozenset()) -> Result:
        """Gets the optimal result given a single agent and valves to ignore."""
        return self.plumber.solve(ignore_set)

    @cached_property
    def best_single_agent_result(self) -> Result:
        """Returns the tuple representing the best single agent result."""
        return self.plumber.solve()

    @cached_property
    def valve_subsets_sorted_by_increasing_cardinality_gap(self) -> list[frozenset[str]]:
        """Gets all subsets of every quiescent valve, sorted by the cardinality gap between the human and elephant."""
        return sorted(list(self.generate_all_subsets_starting_from()), key=lambda subst: abs(len(subst) - len(self.plumber.quiescent_valves)))

    @cached_property
    def start_bound(self) -> int:
        """
        Calculates a reasonable "best so far".

        Uses the result obtained from greedily giving leftover valves to the elephant.
        When the first part of an assignment has no hope of beating the bound, we prune.
        """
        best_single_agent_score, best_single_agent_path = self.best_single_agent_result[0:2]
        best_complement_score = self.plumber.solve(set(best_single_agent_path))[0]
        return best_single_agent_score + best_complement_score

    @cached_property
    def part_one(self) -> int:
        """Returns the answer to part 1."""
        return self.best_single_agent_result[0]

    @cached_property
    def part_two(self) -> int:
        """Returns the answer to part 2."""
        highest_score_ignoring = {}
        best_score = self.start_bound
        best_single_agent_score = self.part_one
        for human_will_ignore in self.valve_subsets_sorted_by_increasing_cardinality_gap:
            if human_will_ignore in highest_score_ignoring:
                continue
            elephant_will_ignore = frozenset(self.plumber.quiescent_valves - human_will_ignore)
            human_score = self.get_single_agent_result(human_will_ignore)[0]
            highest_score_ignoring[human_will_ignore] = human_score
            if human_score + best_single_agent_score < best_score:
                highest_score_ignoring[elephant_will_ignore] = -INF
                continue
            elephant_score = self.get_single_agent_result(elephant_will_ignore)[0]
            highest_score_ignoring[elephant_will_ignore] = elephant_score
            best_score = max(best_score, human_score + elephant_score)
        return best_score


def run_all_tests() -> None:
    """Run all unit tests."""

    test_cases = {
        "example1": (1651, 1707, None),
        "input1": (1850, 2306, None),
        "input2": (1728, 2304, None),
        "input3": (4999999999995, 1000000000304, None),
        "input4": (60, 100, (6, 6)),  # /u/Zerdligham
        "input5": (2640, 2670, None),  # /u/i_have_no_biscuits
        "input6": (13468, 12887, None),  # /u/i_have_no_biscuits
        "input7": (1288, 1484, None),  # /u/i_have_no_biscuits
        "input8": (2400, 3680, None),  # /u/i_have_no_biscuits
    }

    # Part 1
    for filename, test_data in test_cases.items():
        expected, _, turn_setup = test_data
        print(f"{filename: <8} -> {expected}")
        max_turns = 30
        if turn_setup is not None:
            max_turns = turn_setup[0]
        actual = ElephantSolver(TravellingPlumber.from_filename(path=filename, start_valve="AA", max_turns=max_turns)).part_one
        assert actual == expected, f"got {actual} for p1 for {filename} but expected {expected}"

    # Part 2
    for filename, test_data in test_cases.items():
        _, expected, turn_setup = test_data
        print(f"{filename: <8} -> {expected}")
        max_turns = 26
        if turn_setup is not None:
            max_turns = turn_setup[1]
        actual = ElephantSolver(TravellingPlumber.from_filename(path=filename, start_valve="AA", max_turns=max_turns)).part_two
    assert actual == expected, f"got {actual} for p2 for {filename} but expected {expected}"


if __name__ == "__main__":
    run_all_tests()
