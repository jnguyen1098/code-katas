#!/usr/bin/env python3.11
"""Implementation for Advent of Code 2022, Day 16 with BnB."""

from __future__ import annotations

import math
import re
from typing import Iterable

INF = 0x3F3F3F3F
DEFAULT_START_VALVE = 0
BIT_LENGTH = 16

RawValve = tuple[int, int, list[int]]  # name, flow, exits
Valve = tuple[int, int, int]  # name, flow, exits
NAME, FLOW, EXITS = 0, 1, 2

Result = tuple[int, int, int]  # payout, path set, turns_left

# (a - y) * 26 + (b - y)
# 26a - 26y + b - y
# 26a - 27y + b


def valve_to_num(valve: str) -> int:
    """Converts a base-26 valve designation (AA..ZZ) to an integer."""
    return 26 * ord(valve[0]) + ord(valve[1]) - 1755


def num_to_valve(val: int) -> str:
    """Converts an integer [0, 676) back to its valve representation."""
    res = ["A", "A"]

    if val < 26:
        res[1] = chr(65 + val)
    else:
        res[0] = chr(65 + (val // 26) % 26)
        res[1] = chr(65 + (val % 26))

    return "".join(res)


def int_list_to_mask(ints: list[int]) -> int:
    """Converts a list of integers into a bitset."""
    mask = 0
    for num in ints:
        assert 0 <= num < BIT_LENGTH, "Fixed-width constraint violated"
        mask |= 1 << num
    return mask


class TravellingPlumber:
    """Represents a branch-and-bound implementation of AOC 2022, Day 16: Proboscidea Volcanium."""

    def __init__(self, valves: list[Valve], max_turns: int, start_valve_name: int) -> None:
        self.valves = valves
        self.max_turns = max_turns
        self.start_valve_name = start_valve_name
        self.valve_by_name = {valve[0]: valve for valve in self.valves}  # TODO
        self.quiescent_mask = self.get_quiescent_mask()
        self.canonical_graph = self.get_canonical_graph()
        self.maximal_valve_ordering = self.get_maximal_valve_ordering()

    def get_floyd_warshall_closure(self) -> dict[int, dict[int, int]]:
        """Establishes the transitive closure of the graph using the Floyd-Warshall algorithm."""
        from collections import defaultdict
        raw_valve_count = len(self.valves)
        cost_transitive_closure: list[int] = [INF] * raw_valve_count**2

        for valve in self.valve_by_name.values():
            exit_mask = valve[2]  # TODO
            while exit_mask:
                exit_name = int(math.log2(exit_mask))
                cost_transitive_closure[valve[0] * raw_valve_count + exit_name] = 1  # TODO
                exit_mask &= ~(1 << exit_name)

        for k in (valve_names := list(self.valve_by_name.keys())):
            for i in valve_names:
                for j in valve_names:
                    if i == j:
                        continue
                    cost_transitive_closure[i * raw_valve_count + j] = min(
                        cost_transitive_closure[i * raw_valve_count + j],
                        cost_transitive_closure[i * raw_valve_count + k] + cost_transitive_closure[k * raw_valve_count + j],
                    )

        expanded_dict: dict[int, int] = defaultdict(lambda: defaultdict(lambda: INF))

        for x in range(raw_valve_count):
            for y in range(raw_valve_count):
                expanded_dict[x][y] = cost_transitive_closure[x * raw_valve_count + y]
                expanded_dict[y][x] = cost_transitive_closure[x * raw_valve_count + y]

        return expanded_dict

    def get_canonical_graph(self) -> dict[int, dict[int, int]]:
        """
        Takes the transitive closure created by the Floyd-Warshall algorithm and reduces it.

        Now that every shortest cost is found, we only want non-zero interactions.
        """
        cost_transitive_closure = self.get_floyd_warshall_closure()
        canonical_graph: dict[int, dict[int, int]] = {}

        for quiescent_valve_name in range(self.quiescent_mask.bit_count() + 1):
            if quiescent_valve_name not in canonical_graph:
                canonical_graph[quiescent_valve_name] = {}
            for target in range(self.quiescent_mask.bit_count() + 1):
                if target not in canonical_graph:
                    canonical_graph[target] = {}
                canonical_graph[quiescent_valve_name][target] = cost_transitive_closure[quiescent_valve_name][target]
                canonical_graph[target][quiescent_valve_name] = cost_transitive_closure[target][quiescent_valve_name]

        canonical_graph[self.start_valve_name] = {}
        for end in cost_transitive_closure[self.start_valve_name]:
            if not self.quiescent_mask & (1 << end):
                continue
            canonical_graph[self.start_valve_name][end] = cost_transitive_closure[self.start_valve_name][end]

        return canonical_graph

    def get_maximal_valve_ordering(self) -> list[int]:
        """The ordering of valves based on flow."""
        ordering = []
        for i in range(self.quiescent_mask.bit_count()):
            ordering.append(i + 1)
        return sorted(ordering, key=lambda valve_name: self.valve_by_name[valve_name][1], reverse=True)  # TODO

    def get_quiescent_mask(self) -> int:
        """Valves that have non-zero flow."""
        pos = 1
        mask = 0
        for valve in self.valves:
            if valve[1] > 0:  # TODO
                assert pos < BIT_LENGTH, "Fixed-width constraint violated"
                mask |= 1 << pos
                pos += 1
        return mask

    @staticmethod
    def reduce_indices(valves: list[RawValve], start_valve: int, max_turns: int) -> tuple[list[Valve], int, int]:
        """Takes a series of valve integers and creates a monotonically-increasing sequence map."""
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
        new_start_valve = DEFAULT_START_VALVE
        for name, flow, exits in valves:
            if name == start_valve:
                new_start_valve = normalized[name]
            new_name = normalized[name]
            new_exits = 0
            for old_exit in exits:
                new_exits |= 1 << normalized[old_exit]
            new_valves.append((new_name, flow, new_exits))
        return new_valves, new_start_valve, max_turns

    @staticmethod
    def from_filename(*, path: str, start_valve: int, max_turns: int) -> "TravellingPlumber":
        """Parses the valves for the problem from a file."""
        with open(path, "r", encoding="ascii") as file_object:
            lines = [line.rstrip("\n") for line in file_object]
        valves = []
        for line in lines:
            parse = re.findall(r"([A-Z]{2}|\d+)", line)
            name, flow, exit_list = valve_to_num(parse[0]), int(parse[1]), list(map(valve_to_num, parse[2:]))
            valves.append((name, flow, exit_list))
        updated_valves, updated_start_valve, updated_max_turns = TravellingPlumber.reduce_indices(valves, start_valve, max_turns)
        return TravellingPlumber(valves=updated_valves, start_valve_name=updated_start_valve, max_turns=updated_max_turns)

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

        def explore_node(curr_valve: int) -> None:

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
                next_flow = curr_flow + self.valve_by_name[next_valve_name][1]  # TODO
                if best_relief_accum[self.max_turns - next_turns_left] >= next_relief:
                    continue
                curr_valve_set |= 1 << next_valve_name
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
        self.cached_sar: Result | None = None
        self.cached_icg: list[int] | None = None
        self.cached_sb: int | None = None

    def generate_subsets(self) -> Iterable[int]:
        """Iterates all subsets modulo the given cardinality, starting at a certain position within."""
        for i in range(2 ** self.plumber.quiescent_mask.bit_count()):
            yield i << 1

    def get_single_agent_result(self, ignore_mask: int) -> Result:
        """Gets the optimal result given a single agent and valves to ignore."""
        return self.plumber.solve(ignore_mask)

    def get_best_single_agent_result(self) -> Result:
        """Returns the tuple representing the best single agent result."""
        if self.cached_sar is not None:
            return self.cached_sar
        self.cached_sar = self.plumber.solve()
        return self.cached_sar

    def get_valve_subsets_sorted_by_increasing_cardinality_gap(self) -> list[int]:
        """Gets all subsets of every quiescent valve, sorted by the cardinality gap between the human and elephant."""
        if self.cached_icg is not None:
            return self.cached_icg
        self.cached_icg = sorted(self.generate_subsets(), key=lambda subst: abs(subst.bit_count() - self.plumber.get_quiescent_mask().bit_count()))
        return self.cached_icg

    def get_start_bound(self) -> int:
        """
        Calculates a reasonable "best so far".

        Uses the result obtained from greedily giving leftover valves to the elephant.
        When the first part of an assignment has no hope of beating the bound, we prune.
        """
        if self.cached_sb is not None:
            return self.cached_sb
        best_single_agent_score, best_single_agent_path = self.get_best_single_agent_result()[0:2]
        best_complement_score = self.plumber.solve(best_single_agent_path)[0]
        self.cached_sb = best_single_agent_score + best_complement_score
        return self.cached_sb

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
