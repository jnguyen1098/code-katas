#!/usr/bin/env python3.11

from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass

import pytest

import pydantic
from pydantic import BaseModel, Extra, StrictBool, StrictInt, StrictStr

FILENAME = "example1"
# FILENAME = "input1"
ENTRY_VALVE_AA = "AA"

input1_cbe = json.loads("""{
	"DR": {
		"IO": 11,
		"OD": 7,
		"UF": 9,
		"WK": 10,
		"IP": 10,
		"ZJ": 9,
		"NC": 11,
		"DV": 8,
		"CL": 2,
		"CF": 2,
		"SB": 8,
		"DL": 10,
		"PD": 5,
		"CW": 8
	},
	"IO": {
		"DR": 11,
		"OD": 7,
		"UF": 7,
		"WK": 11,
		"IP": 4,
		"ZJ": 9,
		"NC": 2,
		"DV": 3,
		"CL": 9,
		"CF": 13,
		"SB": 9,
		"DL": 3,
		"PD": 6,
		"CW": 9
	},
	"OD": {
		"DR": 7,
		"IO": 7,
		"UF": 2,
		"WK": 7,
		"IP": 3,
		"ZJ": 2,
		"NC": 5,
		"DV": 5,
		"CL": 5,
		"CF": 9,
		"SB": 3,
		"DL": 5,
		"PD": 2,
		"CW": 5
	},
	"UF": {
		"DR": 9,
		"IO": 7,
		"OD": 2,
		"WK": 5,
		"IP": 3,
		"ZJ": 3,
		"NC": 5,
		"DV": 7,
		"CL": 7,
		"CF": 11,
		"SB": 5,
		"DL": 5,
		"PD": 4,
		"CW": 3
	},
	"WK": {
		"DR": 10,
		"IO": 11,
		"OD": 7,
		"UF": 5,
		"IP": 8,
		"ZJ": 8,
		"NC": 10,
		"DV": 8,
		"CL": 8,
		"CF": 12,
		"SB": 4,
		"DL": 10,
		"PD": 5,
		"CW": 2
	},
	"IP": {
		"DR": 10,
		"IO": 4,
		"OD": 3,
		"UF": 3,
		"WK": 8,
		"ZJ": 5,
		"NC": 2,
		"DV": 4,
		"CL": 8,
		"CF": 12,
		"SB": 6,
		"DL": 2,
		"PD": 5,
		"CW": 6
	},
	"ZJ": {
		"DR": 9,
		"IO": 9,
		"OD": 2,
		"UF": 3,
		"WK": 8,
		"IP": 5,
		"NC": 7,
		"DV": 7,
		"CL": 7,
		"CF": 11,
		"SB": 5,
		"DL": 7,
		"PD": 4,
		"CW": 6
	},
	"NC": {
		"DR": 11,
		"IO": 2,
		"OD": 5,
		"UF": 5,
		"WK": 10,
		"IP": 2,
		"ZJ": 7,
		"DV": 3,
		"CL": 9,
		"CF": 13,
		"SB": 8,
		"DL": 2,
		"PD": 6,
		"CW": 8
	},
	"DV": {
		"DR": 8,
		"IO": 3,
		"OD": 5,
		"UF": 7,
		"WK": 8,
		"IP": 4,
		"ZJ": 7,
		"NC": 3,
		"CL": 6,
		"CF": 10,
		"SB": 6,
		"DL": 2,
		"PD": 3,
		"CW": 6
	},
	"CL": {
		"DR": 2,
		"IO": 9,
		"OD": 5,
		"UF": 7,
		"WK": 8,
		"IP": 8,
		"ZJ": 7,
		"NC": 9,
		"DV": 6,
		"CF": 4,
		"SB": 6,
		"DL": 8,
		"PD": 3,
		"CW": 6
	},
	"CF": {
		"DR": 2,
		"IO": 13,
		"OD": 9,
		"UF": 11,
		"WK": 12,
		"IP": 12,
		"ZJ": 11,
		"NC": 13,
		"DV": 10,
		"CL": 4,
		"SB": 10,
		"DL": 12,
		"PD": 7,
		"CW": 10
	},
	"SB": {
		"DR": 8,
		"IO": 9,
		"OD": 3,
		"UF": 5,
		"WK": 4,
		"IP": 6,
		"ZJ": 5,
		"NC": 8,
		"DV": 6,
		"CL": 6,
		"CF": 10,
		"DL": 8,
		"PD": 3,
		"CW": 2
	},
	"DL": {
		"DR": 10,
		"IO": 3,
		"OD": 5,
		"UF": 5,
		"WK": 10,
		"IP": 2,
		"ZJ": 7,
		"NC": 2,
		"DV": 2,
		"CL": 8,
		"CF": 12,
		"SB": 8,
		"PD": 5,
		"CW": 8
	},
	"PD": {
		"DR": 5,
		"IO": 6,
		"OD": 2,
		"UF": 4,
		"WK": 5,
		"IP": 5,
		"ZJ": 4,
		"NC": 6,
		"DV": 3,
		"CL": 3,
		"CF": 7,
		"SB": 3,
		"DL": 5,
		"CW": 3
	},
	"CW": {
		"DR": 8,
		"IO": 9,
		"OD": 5,
		"UF": 3,
		"WK": 2,
		"IP": 6,
		"ZJ": 6,
		"NC": 8,
		"DV": 6,
		"CL": 6,
		"CF": 10,
		"SB": 2,
		"DL": 8,
		"PD": 3
	},
	"AA": {
		"DR": 10,
		"IO": 3,
		"OD": 5,
		"UF": 5,
		"WK": 10,
		"IP": 2,
		"ZJ": 7,
		"NC": 3,
		"DV": 2,
		"CL": 8,
		"CF": 12,
		"SB": 8,
		"DL": 3,
		"PD": 5,
		"CW": 8
	}
}
""")


class Valve(BaseModel):
    name: str
    flow: int
    exits: list[str]

class Problem(BaseModel):
    valves: list[Valve]
    valve_by_name: dict[str, Valve]
    decoy_valves: set[str]
    cost_by_edges: dict[str, dict[str, int]]

    @pydantic.validator("valves", pre=True)
    def validate_valves(cls, value):
        name_counter = defaultdict(int)
        for valve in value:
            if name_counter[valve.name] > 0:
                raise ValueError(f"Duplicate valve {valve.name} detected")
            name_counter[valve.name] += 1
        valve_names = set(name_counter.keys())
        for valve in value:
            for exit_name in valve.exits:
                if exit_name not in valve_names:
                    raise ValueError(f"Non-existent exit {exit_name} detected")
        for valve in value:
            if valve.flow < 0:
                raise ValueError(f"Invalid flow for valve {valve.name}: {valve.flow}")
        for valve in value:
            if valve.name == ENTRY_VALVE_AA and valve.flow != 0:
                raise ValueError(f"Entry valve should have 0 flow")
        return value

    @pydantic.validator("valve_by_name")
    def validate_valve_by_name(cls, value):
        for valve_name, valve in value.items():
            if valve_name != valve.name:
                raise ValueError(f"Dict value for key {valve_name} has bad name {valve.name}")
        return value

    @pydantic.validator("decoy_valves")
    def validate_decoy_valves(cls, value):
        return value

    @pydantic.validator("cost_by_edges")
    def validate_cost_by_edges(cls, value):
        return value

    @pydantic.root_validator(pre=True)
    def validate_all(cls, values):
        values["valves"] = Problem.validate_valves(values["valves"])
        values["valve_by_name"] = {valve.name: valve for valve in values["valves"]}
        values["decoy_valves"] = {valve.name for valve in values["valves"] if not valve.flow}
        values["cost_by_edges"] = get_cost_by_edges(values["valve_by_name"], values["decoy_valves"]) if "cost_by_edges" not in values else values["cost_by_edges"]
        return values

def solve(valves, decoy_valves, cost_by_edges, valve_by_name, *, start_valve=ENTRY_VALVE_AA, taken_dict=None, min_left=None) -> int:
    curr_path = []
    curr_flow = 0
    curr_profit = 0
    minutes_left = 30 if not min_left else min_left
    best_profit = -0x3F3F3F3F
    is_taken = {valve.name: False for valve in valves if valve.name not in decoy_valves} if not taken_dict else taken_dict
    is_taken[start_valve] = True
    max_flow = sum(valve.flow for valve in valves)
    dp = {}
    calls = 0
    best_path = []

    def go(next_valve: str) -> None:
        nonlocal curr_flow
        nonlocal curr_profit
        nonlocal minutes_left
        nonlocal best_profit
        nonlocal calls
        nonlocal best_path

        calls += 1

        if (cache_hit := dp.get(key := (minutes_left, next_valve, curr_profit))) is not None:
            return

        if (attempt := (curr_profit + (curr_flow * minutes_left))) > best_profit:
            best_profit = attempt
            best_path = curr_path[:]

        if minutes_left == 1:
            dp[key] = best_profit
            return

        for valve_name in is_taken.keys():
            if not is_taken[valve_name]:
                if (cost := cost_by_edges[next_valve][valve_name] + 1) > minutes_left:
                    continue
                if ((curr_profit + (curr_flow * cost)) + (max_flow * (minutes_left - cost))) < best_profit:
                    continue
                is_taken[valve_name] = True
                curr_path.append(valve_name)
                curr_profit += (curr_flow * cost)
                curr_flow += valve_by_name[valve_name].flow
                minutes_left -= cost
                go(valve_name)
                minutes_left += cost
                curr_flow -= valve_by_name[valve_name].flow
                curr_profit -= (curr_flow * cost)
                curr_path.pop()
                is_taken[valve_name] = False

        dp[key] = best_profit

    go(start_valve)
    return best_profit, best_path

def get_shortest_path_length(from_valve: str, to_valve: str, valve_by_name: dict[str, Valve], dp):

    key = frozenset((from_valve, to_valve))
    if (cache_hit := dp.get(key)) is not None:
        return cache_hit

    paths = []
    curr_seen = {from_valve}

    def go(next_valve: str):
        if next_valve == to_valve:
            paths.append(len(curr_seen))
            return
        for exit_name in valve_by_name[next_valve].exits:
            if exit_name not in curr_seen:
                curr_seen.add(exit_name)
                go(exit_name)
                curr_seen.remove(exit_name)

    go(from_valve)

    dp[key] = min(paths) if paths else 0
    return dp[key]

def get_cost_by_edges(valve_by_name: dict[str, Valve], decoy_valves: set[str]):
    cost_by_edges = defaultdict(lambda: defaultdict(lambda: 0x3F3F3F3F))
    dp = {}
    for from_valve in valve_by_name:
        for to_valve in valve_by_name:
            if from_valve == to_valve:
                continue
            shortest_path = get_shortest_path_length(from_valve, to_valve, valve_by_name, dp)
            cost_by_edges[from_valve][to_valve] = shortest_path - 1
            cost_by_edges[to_valve][from_valve] = shortest_path - 1

    result = defaultdict(dict)

    for from_node in cost_by_edges.keys():
        if from_node in decoy_valves:
            continue
        for to_node in cost_by_edges[from_node].keys():
            if to_node in decoy_valves:
                continue
            result[from_node][to_node] = cost_by_edges[from_node][to_node]

    for to_node in cost_by_edges[ENTRY_VALVE_AA].keys():
        if to_node in decoy_valves:
            continue
        result[ENTRY_VALVE_AA][to_node] = cost_by_edges[ENTRY_VALVE_AA][to_node]

    return result

def parse_valve_by_name(filename: str, cost_by_edges=None) -> Problem:
    valves = []

    with open(filename) as fp:
        for line in fp:
            match = re.findall(r"(?:[A-Z]{2})|(?:\d+)", line)
            name, flow, exits = match[0], int(match[1]), match[2:]
            valves.append(Valve(name=name, flow=flow, exits=exits))

    return Problem(valves=valves) if not cost_by_edges else Problem(valves=valves, cost_by_edges=cost_by_edges)

def test_parse_valve_by_name() -> None:
    assert parse_valve_by_name("example1").valve_by_name == {
        "AA": Valve(name="AA", flow=0, exits=["DD", "II", "BB"]),
        "BB": Valve(name="BB", flow=13, exits=["CC", "AA"]),
        "CC": Valve(name="CC", flow=2, exits=["DD", "BB"]),
        "DD": Valve(name="DD", flow=20, exits=["CC", "AA", "EE"]),
        "EE": Valve(name="EE", flow=3, exits=["FF", "DD"]),
        "FF": Valve(name="FF", flow=0, exits=["EE", "GG"]),
        "GG": Valve(name="GG", flow=0, exits=["FF", "HH"]),
        "HH": Valve(name="HH", flow=22, exits=["GG"]),
        "II": Valve(name="II", flow=0, exits=["AA", "JJ"]),
        "JJ": Valve(name="JJ", flow=21, exits=["II"]),
    }

def test_get_shortest_path_between() -> None:
    valve_by_name = parse_valve_by_name("example1")

@pytest.mark.parametrize(
    "args, msg",
    [
        ([Valve(name="AA", flow=0, exits=[]), Valve(name="AA", flow=1, exits=[])], "Duplicate"),
        ([Valve(name="AA", flow=0, exits=[]), Valve(name="BB", flow=1, exits=["CC"])], "exist"),
        ([Valve(name="AA", flow=0, exits=[]), Valve(name="BB", flow=-1, exits=[])], "Invalid"),
        ([Valve(name="AA", flow=1, exits=[]), Valve(name="BB", flow=1, exits=[])], "0 flow"),
    ]
)
def test_problem_exceptions(args, msg) -> None:
    with pytest.raises(pydantic.error_wrappers.ValidationError) as exc:
        Problem(valves=args)
    assert msg in str(exc)

def test_example_1():
    parsed = parse_valve_by_name("example1")
    example1 = solve(parsed.valves, parsed.decoy_valves, parsed.cost_by_edges, parsed.valve_by_name, start_valve=ENTRY_VALVE_AA, taken_dict=None, min_left=None)[0]
    assert example1 == 1651, f"Expected 1651 for example but got {example1}"
    print("Success example 1")

def test_input_1():
    parsed = parse_valve_by_name("input1", cost_by_edges=input1_cbe)
    example1 = solve(parsed.valves, parsed.decoy_valves, parsed.cost_by_edges, parsed.valve_by_name, start_valve=ENTRY_VALVE_AA, taken_dict=None, min_left=None)[0]
    assert example1 == 1850, f"Expected 1850 for example but got {example1}"
    print("Success input 1")

# test_example_1()
test_input_1()

def create_mask(all_valves: list[str], blocked_valves: list[str]) -> dict[str, bool]:
    return {valve: (valve in blocked_valves) for valve in all_valves}

def test_example_12():
    parsed = parse_valve_by_name("example1")
    non_decoy_valve_names = {valve.name for valve in parsed.valves if valve.name not in parsed.decoy_valves}
    optimal_path = solve(parsed.valves, parsed.decoy_valves, parsed.cost_by_edges, parsed.valve_by_name, start_valve=ENTRY_VALVE_AA, taken_dict=None, min_left=26)[1]
    print(f"{optimal_path=}")
    exit()
    best_max = -0x3F3F3F3F
    for cutoff in range(len(optimal_path)):
        human_section = optimal_path[:cutoff]
        elephant_section = optimal_path[cutoff:]
        human_score, human_path = solve(parsed.valves, parsed.decoy_valves, parsed.cost_by_edges, parsed.valve_by_name, start_valve=ENTRY_VALVE_AA, taken_dict=create_mask(non_decoy_valve_names, set(human_section)), min_left=26)
        elephant_score, elephant_path = solve(parsed.valves, parsed.decoy_valves, parsed.cost_by_edges, parsed.valve_by_name, start_valve=ENTRY_VALVE_AA, taken_dict=create_mask(non_decoy_valve_names, set(elephant_section)), min_left=26)
        if (combined := human_score + elephant_score) > best_max:
            best_max = combined
            print(human_section, elephant_section)
    assert best_max == 1707, f"Expected 1707 for example but got {best_max}"
    print("Success example 1 part 2")

def test_input_12():
    parsed = parse_valve_by_name("input1")
    non_decoy_valve_names = {valve.name for valve in parsed.valves if valve.name not in parsed.decoy_valves}
    optimal_path = solve(parsed.valves, parsed.decoy_valves, parsed.cost_by_edges, parsed.valve_by_name, start_valve=ENTRY_VALVE_AA, taken_dict=None, min_left=999999999)[1]
    best_max = -0x3F3F3F3F
    for cutoff in range(len(optimal_path)):
        human_section = optimal_path[:cutoff]
        elephant_section = optimal_path[cutoff:]
        human_score, human_path = solve(parsed.valves, parsed.decoy_valves, parsed.cost_by_edges, parsed.valve_by_name, start_valve=ENTRY_VALVE_AA, taken_dict=create_mask(non_decoy_valve_names, set(human_section)), min_left=26)
        elephant_score, elephant_path = solve(parsed.valves, parsed.decoy_valves, parsed.cost_by_edges, parsed.valve_by_name, start_valve=ENTRY_VALVE_AA, taken_dict=create_mask(non_decoy_valve_names, set(elephant_section)), min_left=26)
        if (combined := human_score + elephant_score) > best_max:
            best_max = combined
            print(human_section, elephant_section)
    assert best_max == 2306, f"Expected 2306 for example but got {best_max}"
    print("Success input 1 part 2")

def test_input_22():
    parsed = parse_valve_by_name("input2")
    non_decoy_valve_names = {valve.name for valve in parsed.valves if valve.name not in parsed.decoy_valves}
    optimal_path = solve(parsed.valves, parsed.decoy_valves, parsed.cost_by_edges, parsed.valve_by_name, start_valve=ENTRY_VALVE_AA, taken_dict=None, min_left=26)[1]
    best_max = -0x3F3F3F3F
    elephant_ignore = set(optimal_path)
    human_ignore = non_decoy_valve_names - elephant_ignore
    human_score, human_path = solve(parsed.valves, parsed.decoy_valves, parsed.cost_by_edges, parsed.valve_by_name, start_valve=ENTRY_VALVE_AA, taken_dict=create_mask(non_decoy_valve_names, human_ignore), min_left=26)
    elephant_score, elephant_path = solve(parsed.valves, parsed.decoy_valves, parsed.cost_by_edges, parsed.valve_by_name, start_valve=ENTRY_VALVE_AA, taken_dict=create_mask(non_decoy_valve_names, elephant_ignore), min_left=26)
    best_max = human_score + elephant_score
    assert best_max == 2304, f"Expected 2304 for example but got {best_max}"
    print("Success input 2 part 2")
test_input_22()
