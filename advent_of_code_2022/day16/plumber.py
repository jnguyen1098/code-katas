#!/usr/bin/env python3.11
"""Implementation for Advent of Code 2022, Day 16 with BnB."""

from __future__ import annotations

import itertools
import re
from typing import Iterable

INF = 0x3F3F3F3F
DEFAULT_START_VALVE = 0

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
        self.valve_by_name = {valve[NAME]: valve for valve in self.valves}
        self.cache = {}
        self.cost_between = self.get_cost_between()
        self.quiescent_mask = self.get_quiescent_mask()
        self.canonical_graph = self.get_canonical_graph()
        self.maximal_valve_ordering = self.get_maximal_valve_ordering()

    def get_cost_between(self) -> dict[str, dict[str, int]]:
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
            if left not in expanded_dict:
                expanded_dict[left] = {}
            if right not in expanded_dict:
                expanded_dict[right] = {}
            expanded_dict[left][right] = cost
            expanded_dict[right][left] = cost

        return expanded_dict

    def get_canonical_graph(self) -> dict[str, dict[str, int]]:
        """
        Takes the transitive closure created by the Floyd-Warshall algorithm and reduces it.

        Now that every shortest cost is found, we only want non-zero interactions.
        """
        canonical_graph: dict[str, dict[str, int]] = {}

        for quiescent_valve_name in range(1, 32):
            if self.quiescent_mask & (1 << quiescent_valve_name):
                if quiescent_valve_name not in canonical_graph:
                    canonical_graph[quiescent_valve_name] = {}
                for target in self.cost_between[quiescent_valve_name]:
                    if not self.quiescent_mask & (1 << target):
                        continue
                    if target not in canonical_graph:
                        canonical_graph[target] = {}
                    canonical_graph[quiescent_valve_name][target] = self.cost_between[quiescent_valve_name][target]
                    canonical_graph[target][quiescent_valve_name] = self.cost_between[target][quiescent_valve_name]

        canonical_graph[self.start_valve_name] = {}
        for end in self.cost_between[self.start_valve_name]:
            if not self.quiescent_mask & (1 << end):
                continue
            canonical_graph[self.start_valve_name][end] = self.cost_between[self.start_valve_name][end]

        return canonical_graph

    def get_maximal_valve_ordering(self) -> list[str]:
        """The ordering of valves based on flow."""
        ordering = []
        for i in range(self.quiescent_mask.bit_count()):
            ordering.append(i + 1)
        return sorted(ordering, key=lambda valve_name: self.valve_by_name[valve_name][FLOW], reverse=True)

    def get_quiescent_mask(self) -> set[str]:
        """Valves that have non-zero flow."""
        if (cache_hit := self.cache.get("qm")) is not None:
            return cache_hit
        pos = 1
        mask = 0
        for valve in self.valves:
            if valve[FLOW] > 0:
                assert pos < 32, "32-bit limit reached"
                mask |= (1 << pos)
                pos += 1
        self.cache["qm"] = mask
        return self.cache["qm"]

    @staticmethod
    def reduce_indices(valves: tuple[int, int, list[int]], start_valve: int, max_turns: int) -> tuple[tuple[int, int, list[int]], int, int]:
        idx = 1
        normalized = {}
        new_valves = []
        for name, flow, exits in valves:
            if name == start_valve:
                normalized[name] = 0
            if name not in normalized and flow != 0:
                normalized[name] = idx
                idx += 1
        for name, flow, exits in valves:
            if name not in normalized:
                assert flow == 0
                normalized[name] = idx
                idx += 1
        new_start_valve = None
        for name, flow, exits in valves:
            if name == start_valve:
                new_start_valve = normalized[name]
            new_name = normalized[name]
            new_exits = [normalized[old_exit] for old_exit in exits]
            new_valves.append((new_name, flow, new_exits))
        return new_valves, new_start_valve, max_turns

    @staticmethod
    def from_filename(*, path: str, start_valve: str, max_turns: int) -> "TravellingPlumber":
        """Parses the valves for the problem from a file."""
        with open(path, "r", encoding="ascii") as file_object:
            lines = [line.rstrip("\n") for line in file_object]
        valves = []
        for line in lines:
            parse = re.findall(r"([A-Z]{2}|\d+)", line)
            name, flow, exits = valve_to_num(parse[0]), int(parse[1]), list(map(valve_to_num, parse[2:]))
            valves.append((name, flow, exits))
        valves, start_valve, max_turns = TravellingPlumber.reduce_indices(valves, start_valve, max_turns)
        return TravellingPlumber(valves=valves, start_valve_name=start_valve, max_turns=max_turns)


    # TODO instead of storing valve objects, just use valve indexes
    # TODO do stack stuff for next-state?
    def solve(self, ignore_mask: int = 0) -> Result:
        """
        Solves Advent of Code, 2022, Day 16 for a single agent.

        Pre-processes the valves, a canonical graph, and maximal ordering, all of which rely on
        the maximum turns, start valve, and the valves themselves.
        """

        best_payout = 0
        best_relief_accum = [-1] * self.max_turns
        best_valve_set = 0
        best_turns_left = INF

        curr_flow_stack = [0]
        turns_left_stack = [self.max_turns]
        curr_relief_stack = [0]

        curr_relief_accum = [-1] * self.max_turns
        curr_valve_set = ignore_mask

        def explore_node(curr_valve) -> None:

            nonlocal best_payout
            nonlocal best_relief_accum
            nonlocal best_valve_set
            nonlocal best_turns_left
            nonlocal curr_valve_set

            curr_relief = curr_relief_stack[-1]
            turns_left = turns_left_stack[-1]
            curr_flow = curr_flow_stack[-1]

            if (curr_payout := curr_relief + curr_flow * turns_left) > best_payout:
                best_payout = curr_payout
                best_relief_accum = curr_relief_accum[:]
                best_valve_set = curr_valve_set
                best_turns_left = turns_left

            if turns_left == 1:
                return

            for next_valve_name in self.maximal_valve_ordering:
                if curr_valve_set & (1 << next_valve_name):
                    continue
                activation_cost_in_turns = self.canonical_graph[curr_valve][next_valve_name] + 1
                next_turns_left = turns_left - activation_cost_in_turns
                if turns_left - activation_cost_in_turns < 1:
                    continue
                next_relief = curr_relief + (curr_flow * activation_cost_in_turns)
                next_flow = curr_flow + self.valve_by_name[next_valve_name][FLOW]
                if best_relief_accum[self.max_turns - next_turns_left] >= next_relief:
                    continue
                curr_valve_set |= (1 << next_valve_name)
                curr_flow_stack.append(next_flow)
                curr_relief_accum[self.max_turns - next_turns_left] = next_relief
                curr_relief_stack.append(next_relief)
                turns_left_stack.append(next_turns_left)
                explore_node(next_valve_name)
                turns_left_stack.pop()
                curr_relief_stack.pop()
                curr_flow_stack.pop()
                curr_valve_set &= ~(1 << next_valve_name)

        explore_node(self.start_valve_name)
        return best_payout, best_valve_set, best_turns_left


class ElephantSolver:
    """Container class for solving AOC 2022, Day 16."""

    def __init__(self, plumber: TravellingPlumber) -> None:
        """Instantiates the Elephant Solver."""
        self.plumber = plumber
        self.cache = {}

    def generate_subsets(self) -> Iterable[int]:
        """Iterates all subsets modulo the given cardinality, starting at a certain position within."""
        for i in range(2 ** self.plumber.quiescent_mask.bit_count()):
            yield i << 1

    def get_single_agent_result(self, ignore_mask: int) -> Result:
        """Gets the optimal result given a single agent and valves to ignore."""
        return self.plumber.solve(ignore_mask)

    def get_best_single_agent_result(self) -> Result:
        """Returns the tuple representing the best single agent result."""
        if (cache_hit := self.cache.get("sar")) is not None:
            return cache_hit
        self.cache["sar"] = self.plumber.solve()
        return self.cache["sar"]

    def get_valve_subsets_sorted_by_increasing_cardinality_gap(self) -> list[frozenset[str]]:
        """Gets all subsets of every quiescent valve, sorted by the cardinality gap between the human and elephant."""
        if (cache_hit := self.cache.get("icg")) is not None:
            return cache_hit
        self.cache["icg"] = sorted(self.generate_subsets(), key=lambda subst: abs(subst.bit_count() - self.plumber.get_quiescent_mask().bit_count()))
        return self.cache["icg"]

    def get_start_bound(self) -> int:
        """
        Calculates a reasonable "best so far".

        Uses the result obtained from greedily giving leftover valves to the elephant.
        When the first part of an assignment has no hope of beating the bound, we prune.
        """
        if (cache_hit := self.cache.get("sb")) is not None:
            return cache_hit
        best_single_agent_score, best_single_agent_path = self.get_best_single_agent_result()[0:2]
        best_complement_score = self.plumber.solve(best_single_agent_path)[0]
        self.cache["sb"] = best_single_agent_score + best_complement_score
        return self.cache["sb"]

    def solve_part_one(self) -> int:
        """Returns the answer to part 1."""
        return self.get_best_single_agent_result()[0]

    def solve_part_two(self) -> int:
        """Returns the answer to part 2."""
        highest_score_ignoring = {}
        best_score = self.get_start_bound()
        best_single_agent_score = self.solve_part_one()
        for human_will_ignore in self.get_valve_subsets_sorted_by_increasing_cardinality_gap():
            if human_will_ignore in highest_score_ignoring:
                continue
            elephant_will_ignore = self.plumber.get_quiescent_mask() & ~human_will_ignore
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

    print("Part 1")
    for filename, test_data in test_cases.items():
        expected, _, turn_setup = test_data
        print(f"{filename: <8} -> {expected}")
        max_turns = 30
        if turn_setup is not None:
            max_turns = turn_setup[0]
        actual = ElephantSolver(TravellingPlumber.from_filename(path=filename, start_valve=DEFAULT_START_VALVE, max_turns=max_turns)).solve_part_one()
        assert actual == expected, f"got {actual} for p1 for {filename} but expected {expected}"

    print("\nPart 2")
    for filename, test_data in test_cases.items():
        _, expected, turn_setup = test_data
        print(f"{filename: <8} -> {expected}")
        max_turns = 26
        if turn_setup is not None:
            max_turns = turn_setup[1]
        actual = ElephantSolver(TravellingPlumber.from_filename(path=filename, start_valve=DEFAULT_START_VALVE, max_turns=max_turns)).solve_part_two()
        assert actual == expected, f"got {actual} for p2 for {filename} but expected {expected}"


if __name__ == "__main__":
    run_all_tests()
