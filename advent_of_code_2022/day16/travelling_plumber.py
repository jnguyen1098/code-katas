#!/usr/bin/env python3.11
"""Implementation for Advent of Code 2022, Day 16 with BnB."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections import defaultdict
from pprint import pprint
from typing import Any, Protocol, runtime_checkable

import pydantic
import pytest
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Extra, StrictInt, StrictStr

# TODO: finish interpreter for old impl

INF = 0x3F3F3F3F


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
    def get_lower_bound(self, state: Any) -> Comparable:  # pragma: no cover
        """Gets lower bound for heuristic value of state."""

    @abstractmethod
    def get_upper_bound(self, state: Any) -> Comparable:  # pragma: no cover
        """Gets upper bound for heuristic value of state."""

    @abstractmethod
    def explore_state(self, state: Any) -> Comparable:  # pragma: no cover
        """Explores a state in the exhaustive search."""


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


class State(BaseModel):
    """Represents a node in the exhaustive DFS search."""

    curr_flow: StrictInt
    curr_turn: StrictInt
    curr_valve: StrictStr
    curr_relief: StrictInt


class TravellingPlumber(BoundedBrancher, BaseModel):
    """Represents a branch-and-bound implementation of AOC 2022, Day 16: Proboscidea Volcanium."""

    valves: list[Valve]
    start_valve: StrictStr
    valve_by_name: dict[StrictStr, Valve] | None = None
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
            assert cost == rev_cost
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
        assert mirror_dict == cost_between_valves

        return expanded_dict

    @pydantic.root_validator
    @classmethod
    def create_all_data(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Runs all validators in the right order."""
        if {"valves", "start_valve"} - set(values.keys()):
            raise ValueError(f"Either of {'valves', 'start_valve'} are missing from instantiation...")
        values["valve_by_name"] = TravellingPlumber.create_valve_by_name(values["valves"])
        TravellingPlumber.validate_reachability(values["valve_by_name"], values["start_valve"])
        values["cost_between_valves"] = TravellingPlumber.create_cost_between_valves(values["valve_by_name"])
        values["cost_between_valves"] = TravellingPlumber.validate_cost_between_valves(values["cost_between_valves"])
        return values

    @staticmethod
    def from_lines(*, lines: list[str], start_valve: str) -> TravellingPlumber:
        """Parses the valves for the problem from lines."""
        return TravellingPlumber(valves=[Valve.from_line(line) for line in lines], start_valve=start_valve)

    @staticmethod
    def from_filename(*, filename: str, start_valve: str) -> TravellingPlumber:
        """Parses the valves for the problem from a file."""
        with open(filename, "r", encoding="ascii") as file_object:
            lines = [line.rstrip("\n") for line in file_object]
        return TravellingPlumber.from_lines(lines=lines, start_valve=start_valve)

    def get_lower_bound(self, state: State) -> Comparable:
        """Gets the lower bound for a current state."""
        raise NotImplementedError  # pragma: no cover

    def get_upper_bound(self, state: State) -> Comparable:
        """Gets the upper bound for a current state."""
        raise NotImplementedError  # pragma: no cover

    def explore_state(self, state: State) -> Comparable:
        """Explores the state."""
        raise NotImplementedError  # pragma: no cover


@pytest.fixture(name="example1")
def get_example1() -> TravellingPlumber:
    """Returns a problem instance of the example."""
    return TravellingPlumber.from_filename(filename="example1", start_valve="AA")


@pytest.fixture(name="input1")
def get_input1() -> TravellingPlumber:
    """Returns a problem instance of the input."""
    return TravellingPlumber.from_filename(filename="input1", start_valve="AA")


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
            if i == j:
                continue
            target_closure[from_name][to_name] = closures[valve_names[i]][j]
            target_closure[to_name][from_name] = closures[valve_names[i]][j]

    assert example1.cost_between_valves == target_closure

    assert input1.cost_between_valves is not None
    for valve in input1.valves:
        for exit_valve_name in valve.exits:
            assert input1.cost_between_valves[valve.name][exit_valve_name] == 1
    assert input1.cost_between_valves["ZS"]["SB"] == 2


def test_xd() -> None:
    """Personal sandbox."""
    lmao = TravellingPlumber.from_filename(filename="example1", start_valve="AA")
    pprint(lmao.valve_by_name)
    pprint(lmao.valves)
