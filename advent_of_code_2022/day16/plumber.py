#!/usr/bin/env python3.11
"""Implementation for Advent of Code 2022, Day 16 with BnB."""

from __future__ import annotations

import itertools
import re
import timeit
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import Iterable

import pytest

INF = 0x3F3F3F3F
CURR_FLOW, TURNS_LEFT, CURR_RELIEF = 0, 1, 2
State = tuple[int, int, int]  # curr_flow, turns_left, curr_relief
Result = tuple[int, list[str], int]  # payout, path, turns_left

# import cProfile
# import pstats
# profiler = cProfile.Profile()
# profiler.enable()
# code go here
# profiler.disable()
# stats = pstats.Stats(profiler).sort_stats("tottime")
# stats.print_stats()


@dataclass
class Valve:
    """Valve that enables a flow and can be opened."""

    name: str
    flow: int
    exits: list[str]

    @staticmethod
    def from_line(line: str) -> "Valve":
        """Parses a valve object from a line."""
        if not (match := re.fullmatch(r"Valve ([A-Z]{2})[^=]+=(-?\d+);.*valves? (.*)", line)):
            raise ValueError(f"Could not parse {line=} for class Valve")
        groups = match.groups()
        valve_name, flow, exits = groups[0], int(groups[1]), groups[2].split(", ")
        return Valve(name=valve_name, flow=flow, exits=exits)


@dataclass
class TravellingPlumber:
    """Represents a branch-and-bound implementation of AOC 2022, Day 16: Proboscidea Volcanium."""

    valves: list[Valve]
    max_turns: int
    start_valve_name: str

    @cached_property
    def valve_by_name(self) -> dict[str, Valve]:
        """Takes the valve list and creates a dictionary for easy reference."""
        valve_by_name = {}
        for valve in self.valves:
            if valve.name in valve_by_name:
                raise ValueError(f"Duplicate valve {valve.name} detected")
            valve_by_name[valve.name] = valve
        for valve_name, valve in valve_by_name.items():
            for ex in valve.exits:
                if ex not in valve_by_name:
                    raise ValueError(f"Exit {ex} for valve {valve_name} not present in graph")
        return valve_by_name

    @cached_property
    def cost_between(self) -> dict[str, dict[str, int]]:
        """Establishes the transitive closure of the graph using the Floyd-Warshall algorithm."""
        cost_between = {}

        for valve in self.valve_by_name.values():
            for exit_name in valve.exits:
                cost_between[valve.name, exit_name] = 1

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
            key=lambda valve_name: self.valve_by_name[valve_name].flow,
            reverse=True,
        )

    @cached_property
    def quiescent_valves(self) -> set[str]:
        """Valves that have non-zero flow."""
        return {valve.name for valve in self.valves if valve.flow > 0 and valve.name != self.start_valve_name}

    @staticmethod
    def from_lines(*, lines: list[str], start_valve: str, max_turns: int) -> "TravellingPlumber":
        """Parses the valves for the problem from lines."""
        return TravellingPlumber(valves=[Valve.from_line(line) for line in lines], start_valve_name=start_valve, max_turns=max_turns)

    @staticmethod
    def from_filename(*, path: str, start_valve: str, max_turns: int) -> "TravellingPlumber":
        """Parses the valves for the problem from a file."""
        with open(path, "r", encoding="ascii") as file_object:
            lines = [line.rstrip("\n") for line in file_object]
        return TravellingPlumber.from_lines(lines=lines, start_valve=start_valve, max_turns=max_turns)

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
                next_flow = curr_node[CURR_FLOW] + self.valve_by_name[next_valve_name].flow
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


@pytest.fixture(name="example1")
def get_example1() -> TravellingPlumber:
    """Returns a problem instance of the example."""
    return TravellingPlumber.from_filename(path="example1", start_valve="AA", max_turns=30)


@pytest.fixture(name="input1")
def get_input1() -> TravellingPlumber:
    """Returns a problem instance of the input."""
    return TravellingPlumber.from_filename(path="input1", start_valve="AA", max_turns=30)


# Valve Tests
def test_valve_bad_parse() -> None:
    """Test that invalid lines cause exceptions."""
    with pytest.raises(ValueError) as exc:
        Valve.from_line("")
    assert "parse" in str(exc).casefold()


# Travelling Plumber Tests


def test_plumber_cost_between_names(example1: TravellingPlumber, input1: TravellingPlumber) -> None:
    """Test Floyd-Warshall closure."""
    closures = {
        "AA": [0, 1, 2, 1, 2, 3, 4, 5, 1, 2],
        "BB": [1, 0, 1, 2, 3, 4, 5, 6, 2, 3],
        "CC": [2, 1, 0, 1, 2, 3, 4, 5, 3, 4],
        "DD": [1, 2, 1, 0, 1, 2, 3, 4, 2, 3],
        "EE": [2, 3, 2, 1, 0, 2, 3, 4, 2, 3],
        "FF": [3, 4, 3, 2, 1, 0, 1, 2, 4, 5],
        "GG": [4, 5, 4, 3, 2, 1, 0, 1, 5, 6],
        "HH": [5, 6, 5, 4, 3, 2, 1, 0, 6, 7],
        "II": [1, 2, 3, 2, 3, 4, 5, 6, 0, 1],
        "JJ": [2, 3, 4, 3, 4, 5, 6, 7, 1, 0],
    }
    valve_names = sorted(list(closures.keys()))

    target_closure: dict[str, dict[str, int]] = defaultdict(dict)
    for i, from_name in enumerate(valve_names):
        for j, to_name in enumerate(valve_names):
            if from_name == to_name:
                continue
            target_closure[from_name][to_name] = closures[valve_names[i]][j]
            target_closure[to_name][from_name] = closures[valve_names[i]][j]

    assert example1.cost_between == target_closure

    assert input1.cost_between is not None
    for valve in input1.valves:
        for exit_valve_name in valve.exits:
            assert input1.cost_between[valve.name][exit_valve_name] == 1
    assert input1.cost_between["ZS"]["SB"] == 2


def test_plumber_quiescence(example1: TravellingPlumber) -> None:
    """Test Floyd-Warshall quiescent closure."""
    closures = {
        "AA": [0, 1, 2, 1, 2, 5, 2],
        "BB": [0, 0, 1, 2, 3, 6, 3],
        "CC": [0, 1, 0, 1, 2, 5, 4],
        "DD": [0, 2, 1, 0, 1, 4, 3],
        "EE": [0, 3, 2, 1, 0, 3, 4],
        "HH": [0, 6, 5, 4, 3, 0, 7],
        "JJ": [0, 3, 4, 3, 4, 7, 0],
    }
    valve_names = sorted(list(closures.keys()))

    target_closure: dict[str, dict[str, int]] = defaultdict(dict)
    for i, from_name in enumerate(valve_names):
        for j, to_name in enumerate(valve_names):
            if to_name in {from_name, example1.start_valve_name}:
                continue
            target_closure[from_name][to_name] = closures[valve_names[i]][j]
            if from_name != example1.start_valve_name:
                target_closure[to_name][from_name] = closures[valve_names[i]][j]

    assert example1.canonical_graph == target_closure


def test_example1_solve(example1: TravellingPlumber) -> None:
    """Tests the example1 input."""
    payout, _path, _turns_left = example1.solve()
    assert payout == 1651


def test_input1_solve(input1: TravellingPlumber) -> None:
    """Tests the input1 input."""
    payout, _path, _turns_left = input1.solve()
    assert payout == 1850


def test_input1_benchmarking() -> None:
    """Benchmarks the input1 test."""
    # Unknown setup
    # 2022-12-30 14:13 commit -> 1.5 seconds

    # Running solve()
    # removal of get_children -> 0.75 seconds
    # maximal valve ordering -> 0.7 seconds, 30566 calls
    # maximal valve ordering + remove push -> 0.58 seconds, 31581 calls
    # local profit valve ordering -> 0.65 seconds, 31377 calls
    # local profit valve ordering cached -> 0.42 seconds, 31377 calls

    # With parse included
    # removal of pydantic -> 0.547
    # removal of contracts -> 0.506
    # removal of OO -> 0.499
    # piecewise maximal relief pruning -> 0.119

    iterations = 25

    def stress_test() -> None:
        instance = TravellingPlumber.from_filename(path="input1", start_valve="AA", max_turns=30)
        payout, _path, _turns_left = instance.solve()
        assert payout == 1850, f"got {payout} instead of 1850"

    total_time = timeit.timeit(stress_test, number=iterations)
    average_time = total_time / iterations
    print(f"Average time over {iterations} iterations: {average_time}")


def test_example1_piecewise_answer() -> None:
    """Tests the optimal partition for example1 just to see if it can at least calculate that."""
    instance = TravellingPlumber.from_filename(path="example1", start_valve="AA", max_turns=26)
    # DD BB JJ HH EE CC
    human = instance.solve({"DD", "HH", "EE"})
    elephant = instance.solve({"JJ", "BB", "CC"})
    res = human[0] + elephant[0]
    assert res == 1707


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
