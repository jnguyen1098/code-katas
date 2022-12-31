#!/usr/bin/env python3.11
"""Implementation for Advent of Code 2022, Day 16 with BnB."""

from __future__ import annotations

import itertools
import re
import timeit
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

import pytest

INF = 0x3F3F3F3F
CURR_FLOW, TURNS_LEFT, CURR_RELIEF = 0, 1, 2
State = tuple[int, int, int]  # curr_flow, turns_left, curr_relief
Result = tuple[int, list[str], int]  # payout, path, turns_left


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
    start_valve: str
    valve_by_name: dict[str, Valve] = field(default_factory=dict)
    canonical_graph: dict[str, dict[str, int]] = field(default_factory=dict)
    cost_between_valves: dict[str, dict[str, int]] = field(default_factory=dict)

    @classmethod
    def create_valve_by_name(cls, valves: list[Valve]) -> dict[str, Valve]:
        """Takes the valve list and creates a dictionary for easy reference."""
        valve_by_name = {}
        for valve in valves:
            if valve.name in valve_by_name:
                raise ValueError(f"Duplicate valve {valve.name} detected")
            valve_by_name[valve.name] = valve
        for valve_name, valve in valve_by_name.items():
            for ex in valve.exits:
                if ex not in valve_by_name:
                    raise ValueError(f"Exit {ex} for valve {valve_name} not present in graph")
        return valve_by_name

    @classmethod
    def validate_reachability(cls, valve_by_name: dict[str, Valve], start_valve_name: str) -> None:
        """Validates that the start valve can reach every other valve."""
        start_valve = valve_by_name[start_valve_name]

        reach = {start_valve_name}
        stack = [start_valve]

        while stack:
            popped_valve = stack.pop()
            for valve_exit_name in popped_valve.exits:
                valve_exit = valve_by_name[valve_exit_name]
                if valve_exit_name not in reach:
                    reach.add(valve_exit_name)
                    stack.append(valve_exit)

        if len(reach) != len(valve_by_name):
            sorted_reach = sorted(list(reach))
            sorted_valve_names = sorted(valve_by_name.keys())
            raise ValueError(f"Graph is disjoint; start valve could only reach valves {sorted_reach} out of the valves {sorted_valve_names}")

    @classmethod
    def create_cost_between_valves(cls, valve_by_name: dict[str, Valve]) -> dict[str, dict[str, int]]:
        """Establishes the transitive closure of the graph using the Floyd-Warshall algorithm."""
        cost_between_valves = {}

        for valve in valve_by_name.values():
            for exit_name in valve.exits:
                cost_between_valves[valve.name, exit_name] = 1

        for k in (valve_names := list(valve_by_name.keys())):
            for i in valve_names:
                for j in valve_names:
                    if i == j:
                        continue
                    cost_between_valves[i, j] = min(
                        cost_between_valves.get((i, j), INF),
                        cost_between_valves.get((i, k), INF) + cost_between_valves.get((k, j), INF),
                    )

        expanded_dict: dict[str, dict[str, int]] = {}

        for pair, cost in cost_between_valves.items():
            left, right = pair
            rev_cost = cost_between_valves[right, left]
            assert cost == rev_cost, f"Cost-between-valves is not symmetric between {pair} and {right, left}"
            if left not in expanded_dict:
                expanded_dict[left] = {}
            if right not in expanded_dict:
                expanded_dict[right] = {}
            expanded_dict[left][right] = cost
            expanded_dict[right][left] = cost

        return expanded_dict

    @classmethod
    def create_canonical_graph(cls, cost_between: dict[str, dict[str, int]], valve_dict: dict[str, Valve], start: str) -> dict[str, dict[str, int]]:
        """
        Takes the transitive closure created by the Floyd-Warshall algorithm and reduces it.

        Now that every shortest cost is found, we only want non-zero interactions.
        """
        quiescent_valves = {valve_name for valve_name, valve in valve_dict.items() if valve.flow}
        canonical_graph: dict[str, dict[str, int]] = {}

        for quiescent_valve_name in quiescent_valves:
            if quiescent_valve_name not in canonical_graph:
                canonical_graph[quiescent_valve_name] = {}
            for target in cost_between[quiescent_valve_name]:
                if target not in quiescent_valves:
                    continue
                if target not in canonical_graph:
                    canonical_graph[target] = {}
                canonical_graph[quiescent_valve_name][target] = cost_between[quiescent_valve_name][target]
                canonical_graph[target][quiescent_valve_name] = cost_between[target][quiescent_valve_name]

        assert start not in canonical_graph, "Start node should not have be in canonical graph yet"
        canonical_graph[start] = {}
        for end in cost_between[start]:
            if end not in quiescent_valves:
                continue
            canonical_graph[start][end] = cost_between[start][end]

        return canonical_graph

    @classmethod
    def validate_canonical_graph(cls, canonical: dict[str, dict[str, int]], valve_dict: dict[str, Valve], start: str) -> dict[str, dict[str, int]]:
        """Validates the canonical graph we just made."""
        quiescent_valves = {valve_name for valve_name, valve in valve_dict.items() if valve.flow}
        non_quiescent_valves = set(valve_dict.keys()) - quiescent_valves
        assert quiescent_valves | non_quiescent_valves == set(valve_dict.keys()), "Quiescence should be mutually-exclusive"

        quiescent_valves_reached = set()
        pushed = {start}
        stack = [start]
        for _ in range(len(valve_dict) + 1):
            if not stack:
                break
            popped = stack.pop()
            for exit_valve_name in canonical[popped]:
                if exit_valve_name in non_quiescent_valves or exit_valve_name in pushed:
                    continue
                pushed.add(exit_valve_name)
                quiescent_valves_reached.add(exit_valve_name)
                stack.append(exit_valve_name)
        else:
            raise Exception(f"Timed out after {len(valve_dict)} iterations")  # pragma: no cover

        assert set(canonical.keys()) - {start} == quiescent_valves, "Canonical key mismatch"

        for from_valve in canonical:
            assert set(canonical[from_valve].keys()) == quiescent_valves - {from_valve}, "Canonical graph doesn't have full coverage"

        assert quiescent_valves_reached == quiescent_valves, "Canonical traversal isn't exhaustive"
        return canonical

    def validate_everything_or_crash(self) -> None:
        """Validates everything else I forgot."""
        canonical_valve_names = set(self.canonical_graph.keys()) - {self.start_valve}
        for valve in self.valves:
            if valve.name in canonical_valve_names:
                assert valve.flow > 0, "Raw valve mismatch with canonical graph"
            else:
                assert valve.flow == 0

    def __post_init__(self) -> None:
        """Runs all validators in the right order."""
        self.valve_by_name = TravellingPlumber.create_valve_by_name(self.valves)
        TravellingPlumber.validate_reachability(self.valve_by_name, self.start_valve)
        self.cost_between_valves = TravellingPlumber.create_cost_between_valves(self.valve_by_name)
        self.canonical_graph = TravellingPlumber.create_canonical_graph(
            self.cost_between_valves,
            self.valve_by_name,
            self.start_valve,
        )
        self.canonical_graph = TravellingPlumber.validate_canonical_graph(
            self.canonical_graph,
            self.valve_by_name,
            self.start_valve,
        )
        self.maximal_valve_ordering = sorted(
            set(self.canonical_graph.keys()) - {self.start_valve},
            key=lambda valve_name: self.valve_by_name[valve_name].flow,
            reverse=True,
        )
        self.validate_everything_or_crash()

    @staticmethod
    def from_lines(*, lines: list[str], start_valve: str, max_turns: int) -> "TravellingPlumber":
        """Parses the valves for the problem from lines."""
        return TravellingPlumber(valves=[Valve.from_line(line) for line in lines], start_valve=start_valve, max_turns=max_turns)

    @staticmethod
    def from_filename(*, filename: str, start_valve: str, max_turns: int) -> "TravellingPlumber":
        """Parses the valves for the problem from a file."""
        with open(filename, "r", encoding="ascii") as file_object:
            lines = [line.rstrip("\n") for line in file_object]
        return TravellingPlumber.from_lines(lines=lines, start_valve=start_valve, max_turns=max_turns)

    def solve(self, ignore_set: set[str] | frozenset[str] | None = None) -> Result:

        ignore = ignore_set or set()

        metrics = {
            "goal_states_encountered": 0,
            "children_generated": 0,
            "duplicate_valve_rejections": 0,
            "bound_rejections": 0,
            "total_calls": 0,
        }

        def increment(metric: str) -> None:
            metrics[metric] += 1

        def get_payout(state: State) -> int:
            return state[CURR_RELIEF] + state[CURR_FLOW] * state[TURNS_LEFT]

        start_node = (0, self.max_turns, 0)

        best_payout = get_payout(start_node)
        best_relief_accum = [-1] * self.max_turns
        best_valve_path = []
        best_turns_left = INF

        curr_valve_path = [self.start_valve]
        curr_relief_accum = [-1] * self.max_turns
        curr_valve_set = set()

        def explore_node(curr_node: State, level: int = 0) -> None:

            nonlocal best_payout
            nonlocal best_relief_accum
            nonlocal best_valve_path
            nonlocal best_turns_left

            increment("total_calls")

            curr_flow = curr_node[CURR_FLOW]
            turns_left = curr_node[TURNS_LEFT]
            curr_valve = curr_valve_path[-1]
            curr_relief = curr_node[CURR_RELIEF]

            if (curr_payout := get_payout(curr_node)) > best_payout:
                best_payout = curr_payout
                best_relief_accum = curr_relief_accum[:]
                best_valve_path = curr_valve_path[:]
                best_turns_left = turns_left

            if turns_left == 1:
                increment("goal_states_encountered")
                return

            assert 0 <= turns_left <= self.max_turns
            assert self.canonical_graph is not None
            assert self.valve_by_name is not None

            for next_valve_name in self.maximal_valve_ordering:
                if next_valve_name in ignore or next_valve_name in curr_valve_set:
                    increment("duplicate_valve_rejections")
                    continue
                activation_cost_in_turns = self.canonical_graph[curr_valve][next_valve_name] + 1
                next_turns_left = turns_left - activation_cost_in_turns
                if turns_left - activation_cost_in_turns < 1:
                    continue
                next_relief = curr_relief + (curr_flow * activation_cost_in_turns)
                next_flow = curr_flow + self.valve_by_name[next_valve_name].flow
                next_state = (
                    next_flow,
                    next_turns_left,
                    next_relief,
                )
                increment("children_generated")
                if best_relief_accum[self.max_turns - next_turns_left] >= next_relief:
                    increment("bound_rejections")
                    continue
                curr_valve_set.add(next_valve_name)
                curr_valve_path.append(next_valve_name)
                curr_relief_accum[self.max_turns - next_turns_left] = next_relief
                explore_node(next_state)
                curr_valve_path.pop()
                curr_valve_set.remove(next_valve_name)

        explore_node(start_node)

        """
        for metric_name, value in metrics.items():
            print(f"{metric_name: >30s} -> {value: >10}")
        print()
        print(best_valve_path)
        """
        return best_payout, best_valve_path, best_turns_left


@pytest.fixture(name="example1")
def get_example1() -> TravellingPlumber:
    """Returns a problem instance of the example."""
    return TravellingPlumber.from_filename(filename="example1", start_valve="AA", max_turns=30)


@pytest.fixture(name="input1")
def get_input1() -> TravellingPlumber:
    """Returns a problem instance of the input."""
    return TravellingPlumber.from_filename(filename="input1", start_valve="AA", max_turns=30)


# Valve Tests
def test_valve_bad_parse() -> None:
    """Test that invalid lines cause exceptions."""
    with pytest.raises(ValueError) as exc:
        Valve.from_line("")
    assert "parse" in str(exc).casefold()


# Travelling Plumber Tests


def test_plumber_duplicate_valve() -> None:
    """Test plumber validation for duplicate valve."""
    with pytest.raises(ValueError) as exc:
        TravellingPlumber.from_lines(
            lines=[
                "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
                "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
            ],
            start_valve="AA",
            max_turns=30,
        )
    assert "duplicate" in str(exc).casefold()


def test_plumber_bad_dictionary_invalid_exits() -> None:
    """Test dictionary validation for nonexistent exit."""
    with pytest.raises(ValueError) as exc:
        TravellingPlumber.create_valve_by_name(
            [
                Valve(name="AA", flow=0, exits=["BB"]),
            ]
        )
    assert "not present in graph" in str(exc)


def test_plumber_bad_reachability() -> None:
    """Test reachability of the raw graph."""
    valve_by_name = {
        "AA": Valve(name="AA", flow=0, exits=["BB"]),
        "BB": Valve(name="BB", flow=0, exits=["CC"]),
        "CC": Valve(name="CC", flow=0, exits=[]),
        "FF": Valve(name="FF", flow=0, exits=[]),
    }
    with pytest.raises(ValueError) as exc:
        TravellingPlumber.validate_reachability(valve_by_name, "AA")
    assert "disjoint" in str(exc)


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

    assert example1.cost_between_valves == target_closure

    assert input1.cost_between_valves is not None
    for valve in input1.valves:
        for exit_valve_name in valve.exits:
            assert input1.cost_between_valves[valve.name][exit_valve_name] == 1
    assert input1.cost_between_valves["ZS"]["SB"] == 2


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
            if to_name in {from_name, example1.start_valve}:
                continue
            target_closure[from_name][to_name] = closures[valve_names[i]][j]
            if from_name != example1.start_valve:
                target_closure[to_name][from_name] = closures[valve_names[i]][j]

    assert example1.canonical_graph == target_closure


def test_example1_solve(example1: TravellingPlumber) -> None:
    """Tests the example1 input."""
    payout, path, turns_left = example1.solve()
    assert payout == 1651


def test_input1_solve(input1: TravellingPlumber) -> None:
    """Tests the input1 input."""
    payout, path, turns_left = input1.solve()
    assert payout == 1850


def test_input1_benchmarking() -> None:
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
        instance = TravellingPlumber.from_filename(filename="input1", start_valve="AA", max_turns=30)
        payout, path, turns_left = instance.solve()
        assert payout == 1850, f"got {payout} instead of 1850"

    total_time = timeit.timeit(stress_test, number=iterations)
    average_time = total_time / iterations
    print(f"Average time over {iterations} iterations: {average_time}")


def test_example1_piecewise_answer() -> None:
    instance = TravellingPlumber.from_filename(filename="example1", start_valve="AA", max_turns=26)
    # DD BB JJ HH EE CC
    human = instance.solve({"DD", "HH", "EE"})
    elephant = instance.solve({"JJ", "BB", "CC"})
    res = human[0] + elephant[0]
    assert res == 1707


# input4 only 6 turns; 60 p1, 100 p2, /u/Zerdligham, passes as of commit
# input5 2640, 2670, linearly increasing rates, /u/i_have_no_biscuits, passes as of commit
# input6 13468, 12887, quadratically increasing rates, /u/i_have_no_biscuits, passes as of commit
# input7 1288, 1484, circle, /u/i_have_no_biscuits, passes as of commit
# input8 2400, 3680, clusters, /u/i_have_no_biscuits, passes as of commit
def solve_both(filename: str, turns: tuple[int, int] = (30, 26)) -> tuple[int, int]:
    turns_part_one, turns_part_two = turns
    instance = TravellingPlumber.from_filename(filename=filename, start_valve="AA", max_turns=turns_part_one)
    first = instance.solve()[0]
    instance = TravellingPlumber.from_filename(filename=filename, start_valve="AA", max_turns=turns_part_two)
    all_valves = frozenset(instance.canonical_graph.keys()) - {"AA"}
    all_valves_canonical = sorted(all_valves)

    def get_subset_from_mask(mask: list[int]) -> frozenset[str]:
        return frozenset(itertools.compress(all_valves_canonical, mask))

    def get_nth_mask(idx: int, cardinality: int) -> list[int]:
        return list(map(int, bin(2**cardinality + idx)[3:]))

    def set_to_mask(valve_set: set[str]) -> list[int]:
        mask = []
        for valve in all_valves_canonical:
            if valve in valve_set:
                mask.append(1)
            else:
                mask.append(0)
        return mask

    def mask_to_num(mask: list[int]) -> int:
        return int("".join(map(str, mask)), 2)

    def get_all_subsets_starting_from(start_idx: int = 0) -> Iterable[frozenset[str]]:
        for i in range(2 ** len(all_valves)):
            final_value = (i + start_idx) % (2 ** len(all_valves))
            mask = get_nth_mask(final_value, len(all_valves))
            subset = get_subset_from_mask(mask)
            yield subset

    best_single_agent_score, best_single_agent_path, best_single_agent_turns_left = instance.solve(set())
    print(best_single_agent_score, best_single_agent_path)
    best_complement_score, best_complement_path, best_complement_turns_left = instance.solve(set(best_single_agent_path))
    print(best_complement_score, best_complement_path)

    best_score = best_single_agent_score + best_complement_score

    highest_score_ignoring = {}
    processed = 0
    pruned = 0

    sorted_subsets = sorted(list(get_all_subsets_starting_from()), key=lambda subst: abs(len(subst) - len(all_valves)))

    for subset in sorted_subsets:
        if subset in highest_score_ignoring:
            continue
        human_will_ignore = subset
        elephant_will_ignore = all_valves - human_will_ignore
        human_score, human_path, human_spare = instance.solve(human_will_ignore)
        processed += 1
        if human_score + best_single_agent_score < best_score:
            highest_score_ignoring[elephant_will_ignore] = -INF
            pruned += 1
            continue
        elephant_score, elephant_path, elephant_spare = instance.solve(elephant_will_ignore)
        processed += 1
        highest_score_ignoring[human_will_ignore] = human_score
        highest_score_ignoring[elephant_will_ignore] = elephant_score
        human_args = ", ".join(sorted(elephant_will_ignore))
        ele_args = ", ".join(sorted(human_will_ignore))
        spare_diff = abs(human_spare - elephant_spare)
        if human_score + elephant_score > best_score:
            print(f"{human_args} (human={human_score}) <=={spare_diff}==> (elephant={elephant_score}) {ele_args} ==> {human_score + elephant_score}")
            best_score = human_score + elephant_score
    print(f"{best_score=}, {processed=}, {pruned=}")
    return first, best_score


"""
test_cases = {
    "example1": (1651, 1707, None),
    "input1": (1850, 2306, None),
    "input2": (1728, 2304, None),
    "input3": (4999999999995, 1000000000304, None),
    "input4": (60, 100, (6, 6)),
    "input5": (2640, 2670, None),
    "input6": (13468, 12887, None),
    "input7": (1288, 1484, None),
    "input8": (2400, 3680, None),
}

for filename, test_data in test_cases.items():
    expected_p1, expected_p2, turn_setup = test_data
    if turn_setup is None:
        p1, p2 = solve_both(filename)
    else:
        p1, p2 = solve_both(filename, turn_setup)
    assert p1 == expected_p1, f"got {p1} for p1 for {filename} but expected {expected_p1}"
    assert p2 == expected_p2, f"got {p2} for p2 for {filename} but expected {expected_p2}"

print("we are good!")
"""
