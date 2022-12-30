#!/usr/bin/env python3.11
"""Implementation for Advent of Code 2022, Day 16 with BnB."""

from __future__ import annotations

import re
import timeit
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import Any, Iterable, Protocol, runtime_checkable

import pydantic
import pytest
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Extra, StrictInt, StrictStr

# TODO: finish interpreter for old impl
# TODO: create path simulator and see if I should include it in the abstract
# TODO: determine whether there should be a flag to terminate on first instance of goal node
# TODO: test maximal greedy?

INF = 0x3F3F3F3F
MAX_TURNS = 30  # TODO: fix this!


class BaseModel(PydanticBaseModel):
    """Pydantic strict config."""

    class Config:
        """No extras allowed."""

        extra = Extra.forbid


@runtime_checkable
class Comparable(Protocol):
    """Interface for something that supports comparison."""

    @abstractmethod
    def __lt__(self: Comparable, other: Comparable) -> bool:  # pragma: no cover
        """Return True if self < other else False."""

    @abstractmethod
    def __eq__(self: Comparable, other: object) -> bool:  # pragma: no cover
        """Return True if self == other else False."""


class BoundedBrancher(ABC):
    """Exhaustive searcher that uses branch-and-bound heuristics"""

    @abstractmethod
    def get_start(self) -> Any:  # pragma: no cover
        """Entrypoint for the algorithm."""

    @abstractmethod
    def get_lower_bound(self, state: Any) -> Comparable:  # pragma: no cover
        """Gets lower bound for heuristic value of state."""

    @abstractmethod
    def get_upper_bound(self, state: Any) -> Comparable:  # pragma: no cover
        """Gets upper bound for heuristic value of state."""

    @abstractmethod
    def get_children(self, state: Any) -> Iterable[Any]:  # pragma: no cover
        """Gets children (successors) of the given node."""

    # TODO: remove this?
    @abstractmethod
    def is_goal_state(self, state: Any) -> bool:  # pragma: no cover
        """Given a state, returns True if it's the end state."""

    def solve(self) -> Comparable:
        """Attempts to find the problem using the supplied heuristics."""

        start_node = self.get_start()
        pushed = set()
        best_node = start_node
        lower_bound = self.get_lower_bound(start_node)
        stack = [start_node]

        curr_path = []
        curr_seen = set()

        while stack:
            curr_node = stack.pop()
            if curr_node > best_node:
                best_node = curr_node
            if self.is_goal_state(curr_node):
                continue
            for child_node in self.get_children(curr_node):
                if child_node not in pushed:
                    pushed.add(child_node)
                    if (upper_bound := self.get_upper_bound(child_node)) < lower_bound:
                        continue
                    stack.append(child_node)

        return best_node


class Valve(BaseModel):
    """Valve that enables a flow and can be opened."""

    name: StrictStr
    flow: StrictInt
    exits: list[StrictStr]

    @staticmethod
    def from_line(line: str) -> Valve:
        """Parses a valve object from a line."""
        if not (match := re.fullmatch(r"Valve ([A-Z]{2})[^=]+=(-?\d+);.*valves? (.*)", line)):
            raise ValueError(f"Could not parse {line=} for class Valve")
        groups = match.groups()
        valve_name, flow, exits = groups[0], int(groups[1]), groups[2].split(", ")
        return Valve(name=valve_name, flow=flow, exits=exits)

    @pydantic.root_validator(pre=True)
    @classmethod
    def validate_all(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validates the arguments of the valve."""
        name, flow, exits = values["name"], values["flow"], values["exits"]
        if flow < 0:
            raise ValueError(f"Negative {flow=} not allowed")
        if name in exits:
            raise ValueError(f"Circular valve with self-exit not allowed ({name=}, {flow=}, {exits=})")
        return values


@dataclass
class State:
    """Represents a node in the exhaustive DFS search."""

    curr_flow: int
    curr_turn: int
    curr_valve: str
    curr_relief: int
    curr_payout: int = 0

    def __post_init__(self) -> None:
        self.curr_payout = self.curr_relief + (self.curr_flow * (MAX_TURNS - self.curr_turn + 1))

    def __hash__(self) -> int:
        return hash((self.curr_flow, self.curr_turn, self.curr_valve, self.curr_relief))

    def __lt__(self, other) -> bool:
        return other.curr_payout > self.curr_payout


class TravellingPlumber(BoundedBrancher, BaseModel):
    """Represents a branch-and-bound implementation of AOC 2022, Day 16: Proboscidea Volcanium."""

    valves: list[Valve]
    max_turns: StrictInt
    start_valve: StrictStr
    max_flow: StrictInt | None
    valve_by_name: dict[StrictStr, Valve] | None = None
    canonical_graph: dict[StrictStr, dict[StrictStr, StrictInt]] | None = None
    cost_between_valves: dict[StrictStr, dict[StrictStr, StrictInt]] | None = None

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
    def create_cost_between_valves(cls, valve_by_name: dict[str, Valve]) -> dict[tuple[str, str], int]:
        """Establishes the transitive closure of the graph using the Floyd-Warshall algorithm."""
        dist = {}

        for valve in valve_by_name.values():
            valve_name = valve.name
            for exit_name in valve.exits:
                dist[valve_name, exit_name] = 1

        for k in (valve_names := list(valve_by_name.keys())):
            for i in valve_names:
                for j in valve_names:
                    if i == j:
                        continue
                    dist[i, j] = min(dist.get((i, j), INF), dist.get((i, k), INF) + dist.get((k, j), INF))

        return dist

    @classmethod
    def validate_cost_between_valves(cls, cost_between_valves: dict[tuple[str, str], int]) -> dict[str, dict[str, int]]:
        """Validates the consistency of the Floyd-Warshall closure."""
        expanded_dict: dict[str, dict[str, int]] = {}

        for pair, cost in cost_between_valves.items():
            left, right = pair
            rev_pair = right, left
            rev_cost = cost_between_valves[rev_pair]
            assert cost == rev_cost, "Cost-between-valves is not symmetric"
            if left not in expanded_dict:
                expanded_dict[left] = {}
            if right not in expanded_dict:
                expanded_dict[right] = {}
            expanded_dict[left][right] = cost
            expanded_dict[right][left] = cost

        mirror_dict = {}
        for from_valve, target in expanded_dict.items():
            for to_valve in target:
                mirror_dict[from_valve, to_valve] = expanded_dict[from_valve][to_valve]
                mirror_dict[to_valve, from_valve] = expanded_dict[to_valve][from_valve]
        assert mirror_dict == cost_between_valves, "Dogfooding failed"

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
        for _ in range(len(valve_dict)):
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

    @classmethod
    def validate_everything_or_crash(cls, values: dict[str, Any]) -> None:
        """Validates everything else I forgot."""
        canonical_valve_names = set(values["canonical_graph"].keys()) - {values["start_valve"]}
        for valve in values["valves"]:
            if valve.name in canonical_valve_names:
                assert valve.flow > 0, "Raw valve mismatch with canonical graph"
            else:
                assert valve.flow == 0

    @pydantic.root_validator
    @classmethod
    def create_all_data(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Runs all validators in the right order."""
        if (required_arguments := {"valves", "start_valve", "max_turns"}) - set(values.keys()):
            raise ValueError(f"Either of {required_arguments} are missing from instantiation...")
        values["valve_by_name"] = TravellingPlumber.create_valve_by_name(values["valves"])
        TravellingPlumber.validate_reachability(values["valve_by_name"], values["start_valve"])
        values["cost_between_valves"] = TravellingPlumber.create_cost_between_valves(values["valve_by_name"])
        values["cost_between_valves"] = TravellingPlumber.validate_cost_between_valves(values["cost_between_valves"])
        values["canonical_graph"] = TravellingPlumber.create_canonical_graph(
            values["cost_between_valves"], values["valve_by_name"], values["start_valve"]
        )
        values["canonical_graph"] = TravellingPlumber.validate_canonical_graph(
            values["canonical_graph"], values["valve_by_name"], values["start_valve"]
        )
        values["max_flow"] = sum(valve.flow for valve in values["valves"])
        TravellingPlumber.validate_everything_or_crash(values)
        return values

    @staticmethod
    def from_lines(*, lines: list[str], start_valve: str, max_turns: int) -> TravellingPlumber:
        """Parses the valves for the problem from lines."""
        return TravellingPlumber(valves=[Valve.from_line(line) for line in lines], start_valve=start_valve, max_turns=max_turns)

    @staticmethod
    def from_filename(*, filename: str, start_valve: str, max_turns: int) -> TravellingPlumber:
        """Parses the valves for the problem from a file."""
        with open(filename, "r", encoding="ascii") as file_object:
            lines = [line.rstrip("\n") for line in file_object]
        return TravellingPlumber.from_lines(lines=lines, start_valve=start_valve, max_turns=max_turns)

    def get_start(self) -> State:
        """Generates a start state."""
        return State(curr_flow=0, curr_turn=1, curr_valve=self.start_valve, curr_relief=0)

    def get_lower_bound(self, state: State) -> Comparable:
        """Gets the lower bound for a current state."""
        return state.curr_payout

    def get_upper_bound(self, state: State) -> Comparable:
        """Gets the upper bound for a current state."""
        return state.curr_relief + (self.max_turns - state.curr_turn + 1) * self.max_flow

    def is_goal_state(self, state: State) -> bool:
        """Returns whether the state is terminal."""
        return state.curr_turn == self.max_turns + 1

    def get_children(self, state: State) -> Iterable[State]:
        """Generates children (successors)."""
        curr_flow = state.curr_flow
        curr_turn = state.curr_turn
        curr_valve = state.curr_valve
        curr_relief = state.curr_relief

        assert 1 <= curr_turn <= self.max_turns, f"{curr_turn=} out of bounds; max_turns={self.max_turns}"

        turns_left = self.max_turns - curr_turn + 1

        assert self.canonical_graph is not None
        assert self.valve_by_name is not None
        for next_valve_name in self.canonical_graph[curr_valve].keys():
            next_valve_distance = self.canonical_graph[curr_valve][next_valve_name]
            next_valve_cost = next_valve_distance + 1
            next_turn = curr_turn + next_valve_cost
            yield State(
                curr_flow=curr_flow + self.valve_by_name[next_valve_name].flow,
                curr_turn=next_turn,
                curr_valve=next_valve_name,
                curr_relief=curr_relief + (curr_flow * next_valve_cost),
            )

    def solve(self) -> Comparable:
        start_node = self.get_start()

        best_total_relief_node = start_node

        curr_valve_path = [self.start_valve]
        curr_valve_set = set()
        states_pushed = set()

        metrics = {
            "goal_states_encountered": 0,
            "children_generated": 0,
            "cached_state_hits": 0,
            "wait_rejections": 0,
            "duplicate_valve_rejections": 0,
            "bound_rejections": 0,
            "total_calls": 0,
        }
        def increment(metric: str) -> None:
            metrics[metric] += 1

        def explore_node(curr_node: State, level: int = 0) -> None:

            nonlocal best_total_relief_node

            increment("total_calls")

            best_total_relief_node = max(best_total_relief_node, curr_node)

            if self.is_goal_state(curr_node):
                increment("goal_states_encountered")
                return

            for child_node in self.get_children(curr_node):

                child_valve = child_node.curr_valve
                increment("children_generated")

                if child_node in states_pushed:
                    increment("cached_state_hits")
                    continue
                states_pushed.add(child_node)

                if child_node.curr_turn > self.max_turns + 1:
                    increment("wait_rejections")
                    continue

                if child_valve in curr_valve_set:
                    increment("duplicate_valve_rejections")
                    continue

                if (upper_bound := self.get_upper_bound(child_node)) < self.get_lower_bound(best_total_relief_node):
                    increment("bound_rejections")
                    continue

                curr_valve_set.add(child_valve)
                curr_valve_path.append(child_valve)
                explore_node(child_node)
                curr_valve_path.pop()
                curr_valve_set.remove(child_valve)

        explore_node(start_node)

        for metric_name, value in metrics.items():
            print(f"{metric_name: >30s} -> {value: >10}")

        return best_total_relief_node


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


def test_valve_circular_parse() -> None:
    """Test that valves with self-referential exits are not allowed."""
    with pytest.raises(ValueError) as exc:
        Valve.from_line("Valve AA has flow rate=0; tunnels lead to valve AA")
    assert "circular" in str(exc).casefold()


def test_valve_negative_flow() -> None:
    """Test that valves with negative flow are rejected."""
    with pytest.raises(ValueError) as exc:
        Valve.from_line("Valve AA has flow rate=-1; tunnels lead to valve BB")
    assert "negative" in str(exc).casefold()


# Travelling Plumber Tests
def test_plumber_missing_vars() -> None:
    """Ensures a throw when we forget to include a required variable."""
    with pytest.raises(ValueError) as exc:
        TravellingPlumber(
            lines=[
                "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
                "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
            ],
        )
    assert "missing from instantiation" in str(exc)
    with pytest.raises(ValueError) as exc:
        TravellingPlumber(
            start_valve="AA",
        )
    assert "missing from instantiation" in str(exc)


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


def test_plumber_is_goal_state(example1: TravellingPlumber) -> None:
    """Test goal state detection."""
    goal_state = State(curr_flow=100, curr_turn=31, curr_valve="AA", curr_relief=100)
    assert example1.is_goal_state(goal_state)
    unfinished_state = State(curr_flow=10034, curr_turn=30, curr_valve="BB", curr_relief=1003234)
    assert not example1.is_goal_state(unfinished_state)
    unfinished_state_2 = State(curr_flow=10034, curr_turn=1, curr_valve="BB", curr_relief=1003234)
    assert not example1.is_goal_state(unfinished_state_2)


def test_plumber_get_children(example1: TravellingPlumber) -> None:
    """Tests that the children generator works."""
    start_state = State(curr_flow=0, curr_turn=1, curr_valve="AA", curr_relief=0)
    assert set(example1.get_children(start_state)) == {
        State(curr_flow=13, curr_turn=3, curr_valve="BB", curr_relief=0),
        State(curr_flow=2, curr_turn=4, curr_valve="CC", curr_relief=0),
        State(curr_flow=20, curr_turn=3, curr_valve="DD", curr_relief=0),
        State(curr_flow=3, curr_turn=4, curr_valve="EE", curr_relief=0),
        State(curr_flow=22, curr_turn=7, curr_valve="HH", curr_relief=0),
        State(curr_flow=21, curr_turn=4, curr_valve="JJ", curr_relief=0),
    }
    assert set(example1.get_children(State(curr_flow=3, curr_turn=4, curr_valve="EE", curr_relief=0))) == {
        State(curr_flow=16, curr_turn=8, curr_valve="BB", curr_relief=12),
        State(curr_flow=5, curr_turn=7, curr_valve="CC", curr_relief=9),
        State(curr_flow=23, curr_turn=6, curr_valve="DD", curr_relief=6),
        State(curr_flow=25, curr_turn=8, curr_valve="HH", curr_relief=12),
        State(curr_flow=24, curr_turn=9, curr_valve="JJ", curr_relief=15),
    }


def test_get_start(example1: TravellingPlumber) -> None:
    """Tests start state generation."""
    assert example1.get_start() == State(curr_flow=0, curr_turn=1, curr_valve="AA", curr_relief=0)

def test_example1_solve(example1: TravellingPlumber) -> None:
    """Tests the example1 input."""
    solve_node = example1.solve()
    assert solve_node.curr_payout == 1651

def test_input1_solve(input1: TravellingPlumber) -> None:
    """Tests the input1 input."""
    print(timeit.timeit(lambda: input1.solve(), number=10))
    assert False
    # solve_node = input1.solve()
    # assert solve_node.curr_payout == 1850 + 1
