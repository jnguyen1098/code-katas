#!/usr/bin/env python3.11
"""Implementation for Advent of Code 2022, Day 16 with BnB."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from pprint import pprint
from typing import Any, Protocol, runtime_checkable

import pydantic
import pytest
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Extra, StrictInt, StrictStr


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
    valve_by_name: dict[StrictStr, Valve] | None = None

    @pydantic.root_validator(pre=True)
    @classmethod
    def create_valve_dictionary(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Takes the valve list and creates a dictionary for easy reference."""
        valves = values["valves"]
        valve_by_name = {}
        for valve in valves:
            if valve.name in valve_by_name:
                raise ValueError(f"Duplicate valve {valve.name} detected")
            valve_by_name[valve.name] = valve
        values["valve_by_name"] = valve_by_name
        return values

    @pydantic.validator("valve_by_name")
    @classmethod
    def validate_valve_dictionary(cls, valve_by_name: dict[str, Valve]) -> dict[str, Valve]:
        """Validates the data consistency of the valve dictionary."""
        for valve_name, valve in valve_by_name.items():
            if valve_name != valve.name:
                raise ValueError(f"Key {valve_name} doesn't match valve object name {valve.name}")
            for ex in valve.exits:
                if ex not in valve_by_name:
                    raise ValueError(f"Exit {ex} for valve {valve_name} not present in graph")
        return valve_by_name

    @staticmethod
    def from_lines(lines: list[str]) -> TravellingPlumber:
        """Parses the valves for the problem from lines."""
        return TravellingPlumber(valves=[Valve.from_line(line) for line in lines])

    @staticmethod
    def from_filename(filename: str) -> TravellingPlumber:
        """Parses the valves for the problem from a file."""
        with open(filename, "r", encoding="ascii") as file_object:
            lines = [line.rstrip("\n") for line in file_object]
        return TravellingPlumber.from_lines(lines)

    def get_lower_bound(self, state: State) -> Comparable:
        """Gets the lower bound for a current state."""
        raise NotImplementedError  # pragma: no cover

    def get_upper_bound(self, state: State) -> Comparable:
        """Gets the upper bound for a current state."""
        raise NotImplementedError  # pragma: no cover

    def explore_state(self, state: State) -> Comparable:
        """Explores the state."""
        raise NotImplementedError  # pragma: no cover


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
def test_plumber_duplicate_valve() -> None:
    """Test plumber validation for duplicate valve."""
    with pytest.raises(ValueError) as exc:
        TravellingPlumber.from_lines(
            [
                "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
                "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
            ]
        )
    assert "duplicate" in str(exc).casefold()


def test_plumber_bad_dictionary_name_matching() -> None:
    """Test dictionary validation for bad name."""
    with pytest.raises(ValueError) as exc:
        TravellingPlumber.validate_valve_dictionary(
            {
                "AA": Valve(name="BB", flow=0, exits=[]),
            }
        )
    assert "doesn't match valve object name" in str(exc)


def test_plumber_bad_dictionary_invalid_exits() -> None:
    """Test dictionary validation for nonexistent exit."""
    with pytest.raises(ValueError) as exc:
        TravellingPlumber.validate_valve_dictionary(
            {
                "AA": Valve(name="AA", flow=0, exits=["BB"]),
            }
        )
    assert "not present in graph" in str(exc)


def test_xd() -> None:
    """Personal sandbox."""
    lmao = TravellingPlumber.from_filename("example1")
    pprint(lmao.valve_by_name)
    pprint(lmao.valves)
