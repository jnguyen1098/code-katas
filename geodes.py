#!/usr/bin/env python3.11
"""Allocates resources in the 0/1 AOC Day 19 2022 Knapsack Question."""
 
from __future__ import annotations
 
import math
import operator
from dataclasses import dataclass
from typing import Any, Callable, Generator
 
 
@dataclass
class Kernel:
    """Represents a tuple with modified arithmetic logic."""
 
    data: tuple[int, ...]
 
    def to_list(self) -> list[int]:
        """Converts Kernel to list."""
        return list(self.data)
 
    def __add__(self, other: Kernel) -> Kernel:
        """Adds every member of one Kernel to another."""
        return Kernel(tuple(map(operator.add, self.data, other.data)))
 
    def __sub__(self, other: Kernel) -> Kernel:
        return Kernel(tuple(map(operator.sub, self.data, other.data)))
 
    def __mul__(self, other: Kernel) -> Kernel:
        return Kernel(tuple(map(operator.mul, self.data, other.data)))
 
    def scalar_mult(self, other: int) -> Kernel:
        """Takes the scalar multiplication of the kernel with an integer."""
        return Kernel(tuple(arg * other for arg in self.data))
 
    def __getitem__(self, key: int) -> int:
        return self.data.__getitem__(key)
 
    def __setitem__(self, key: int, value: int) -> None:
        raise TypeError(f"Cannot modify Kernel ({key=} {value=})")
 
    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        for num in self.data:
            yield ("", num)
 
    def __hash__(self) -> int:
        return hash(self.data)
 
    def __len__(self) -> int:
        return len(self.data)
 
 
ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
 
 
def create_cost_dictionary(*args: int) -> dict[int, Kernel]:
    """Takes the raw input from AOC and converts it to a cost kernel dictionary."""
    ore_ore, cla_ore, obs_ore, obs_cla, geo_ore, geo_obs = args
    return {
        ORE: Kernel((ore_ore, 0, 0, 0)),
        CLAY: Kernel((cla_ore, 0, 0, 0)),
        OBSIDIAN: Kernel((obs_ore, obs_cla, 0, 0)),
        GEODE: Kernel((geo_ore, 0, geo_obs, 0)),
    }
 
 
def solve_blueprint(*args: int) -> int:
    """Wrapper function for solving the blueprint value."""
    max_turns, blueprint_number, ore_ore, cla_ore, obs_ore, obs_clay, geo_ore, geo_obs = args
    return optimize_geodes(max_turns, blueprint_number, create_cost_dictionary(ore_ore, cla_ore, obs_ore, obs_clay, geo_ore, geo_obs))
 
 
def optimize_geodes(max_turns: int, blueprint_number: int, cost_of: dict[int, Kernel]) -> int:
    """Takes turns, a blueprint number, and a cost dictionary, then optimizes robot flow."""
 
    resources = [
        GEODE,
        OBSIDIAN,
        CLAY,
        ORE,
    ]
 
    max_atomic_cost_for = {
        ORE: max(kernel[ORE] for kernel in cost_of.values()),
        CLAY: max(kernel[CLAY] for kernel in cost_of.values()),
        OBSIDIAN: max(kernel[OBSIDIAN] for kernel in cost_of.values()),
        GEODE: max_turns,
    }
 
    identity_of = {
        ORE: Kernel((1, 0, 0, 0)),
        CLAY: Kernel((0, 1, 0, 0)),
        OBSIDIAN: Kernel((0, 0, 1, 0)),
        GEODE: Kernel((0, 0, 0, 1)),
    }
 
    can_buy: dict[int, Callable[[Kernel], bool]] = {
        ORE: lambda balance: balance[ORE] >= cost_of[ORE][ORE],
        CLAY: lambda balance: balance[ORE] >= cost_of[CLAY][ORE],
        OBSIDIAN: lambda balance: balance[ORE] >= cost_of[OBSIDIAN][ORE] and balance[CLAY] >= cost_of[OBSIDIAN][CLAY],
        GEODE: lambda balance: balance[OBSIDIAN] >= cost_of[GEODE][OBSIDIAN] and balance[ORE] >= cost_of[GEODE][ORE],
    }
 
    def useless_purchase(resource_id: int, turns_left: int, balance: Kernel, flow: Kernel) -> bool:
        if flow[resource_id] >= max_atomic_cost_for[resource_id]:
            return True
        payout = balance + flow.scalar_mult(turns_left)
        return (payout[resource_id] / turns_left) >= float(max_atomic_cost_for[resource_id])
 
    def should_buy(resource_id: int, turns_left: int, balance: Kernel, flow: Kernel) -> bool:
        return not useless_purchase(resource_id, turns_left, balance, flow)
 
    can_wait_for: dict[int, Callable[[Kernel], bool]] = {
        ORE: lambda flow: True,
        CLAY: lambda flow: True,
        OBSIDIAN: lambda flow: flow[CLAY] > 0,
        GEODE: lambda flow: flow[OBSIDIAN] > 0,
    }
 
    pruned = -1
 
    turn_deficit_for: dict[int, Callable[[Kernel, Kernel], int]] = {
        GEODE: lambda balance, flow: max(
            math.ceil((cost_of[GEODE][ORE] - balance[ORE]) / flow[ORE]),
            math.ceil((cost_of[GEODE][OBSIDIAN] - balance[OBSIDIAN]) / flow[OBSIDIAN]),
        ),
        OBSIDIAN: lambda balance, flow: max(
            math.ceil((cost_of[OBSIDIAN][ORE] - balance[ORE]) / flow[ORE]),
            math.ceil((cost_of[OBSIDIAN][CLAY] - balance[CLAY]) / flow[CLAY]),
        ),
        CLAY: lambda balance, flow: math.ceil((cost_of[CLAY][ORE] - balance[ORE]) / flow[ORE]),
        ORE: lambda balance, flow: math.ceil((cost_of[ORE][ORE] - balance[ORE]) / flow[ORE]),
    }
 
    result_by_state: dict[tuple[int, Kernel, Kernel], int] = {}
 
    def get_geode_score(turns_left: int, balance: Kernel, flow: Kernel) -> int:
        return balance[GEODE] + flow[GEODE] * turns_left + (turns_left * (turns_left + 1)) // 2
 
    def get_geode_payout(turns_left: int, balance: Kernel, flow: Kernel) -> int:
        return balance[GEODE] + flow[GEODE] * turns_left
 
    # TODO: implement proper ordering
    def get_resource_order(turns_left: int, balance: Kernel, flow: Kernel) -> list[int]:
        return resources
 
    best_geode_payout = -1
    all_calls = 0
    hot_calls = 0
    cold_calls = 0
 
    def solve(turns_left: int, balance: Kernel, flow: Kernel) -> int:
        nonlocal best_geode_payout
        nonlocal all_calls
        nonlocal hot_calls
        nonlocal cold_calls
 
        all_calls += 1
 
        # If result is cached, return and mark as a hot call, else cold
        if cache_hit := result_by_state.get(key := (turns_left, balance, flow)):
            hot_calls += 1
            return cache_hit
        cold_calls += 1
 
        # Calculate underestimate for an impossible scenario where you buy geode robot every turn,
        # then keep a running max for this. We will use this to prune states that have no hope of
        # actually succeeding. If a state is incapable of generating enough geodes even if given
        # infinite resources, then there is literally no hope for said universe, so we prune it.
        #
        # This is done right after the cache check. Assuming all results are correctly cached, this
        # guarantees that every cache hit will already have its geode rating recorded.
        best_geode_payout = max(best_geode_payout, get_geode_payout(turns_left, balance, flow))
 
        # From this point on, we are forced to progress. This means we update the balance.
        updated_balance = balance + flow
 
        # Invariant case; there is nothing to do at this turn but reap what you have.
        # This is because robot gains only come in the following turns.
        if turns_left == 1:
            result_by_state[key] = updated_balance[GEODE]
            return result_by_state[key]
 
        # Explore the state-space not by advancing turn-by-turn, but resource-by-resource.
        # Either we have a resource we can buy next, or we can't. This is done by calculating
        # how many turns are required for a certain resource. This means if you need 40 clay for
        # an obsidian robot but you only have 2, and it's turn 23 of 24, don't bother waiting.
        #
        # In such a case, we aim to wait until the end of time. This also allows us to weigh
        # situations where, for example, we don't want to buy an ore robot that costs 4 ore on
        # turn 23 of 24, as it will never pay itself back.
        geode_counts = []
 
        for resource in get_resource_order(turns_left, balance, flow):
 
            # If not enough turns to wait, skip
            if not can_wait_for[resource](flow):
                continue
 
            # If we can't buy, then we skip ahead until we can, then examine that
            if not can_buy[resource](balance):
                turns_to_wait = turn_deficit_for[resource](balance, flow)
                balance_after_waiting = balance + (flow.scalar_mult(turns_to_wait))
                next_turns_left = turns_left - turns_to_wait
                geode_score = get_geode_score(next_turns_left, balance_after_waiting, flow)
                if next_turns_left > 0 and geode_score > best_geode_payout:
                    if (geode_count := solve(next_turns_left, balance_after_waiting, flow)) != pruned:
                        geode_counts.append(geode_count)
                continue
 
            # If we can buy it, we only buy it if we can benefit from its flow.
            # For example, if the highest ore cost is 4, then we cannot spend more than 4 ore per
            # turn, as only 1 robot can be bought per turn. This means our ore robot limit is 4.
            if should_buy(resource, turns_left, balance, flow):
                balance_after_buying = updated_balance - cost_of[resource]
                flow_after_buying = flow + identity_of[resource]
                if get_geode_score(turns_left - 1, balance_after_buying, flow_after_buying) > best_geode_payout:
                    if (geode_count := solve(turns_left - 1, balance_after_buying, flow_after_buying)) != pruned:
                        geode_counts.append(geode_count)
 
        # Next, we examine the state where we stall entirely
        balance_after_stall = balance + (flow.scalar_mult(turns_left))
        if get_geode_score(turns_left - turns_left, balance_after_stall, flow) > best_geode_payout:
            if (geode_count := solve(turns_left - turns_left, balance_after_stall, flow)) != pruned:
                geode_counts.append(geode_count)
 
        # Finally, if no promising states were found, we prune the parent branch entirely
        if not geode_counts:
            result_by_state[key] = pruned
            return result_by_state[key]
 
        # We cache and return the max geode count
        most_geodes = max(geode_counts)
        result_by_state[key] = most_geodes
        return result_by_state[key]
 
    best_geode_count = solve(max_turns, Kernel((0, 0, 0, 0)), Kernel((1, 0, 0, 0)))
    total_calls = hot_calls + cold_calls
    assert total_calls == all_calls
    print(f"{hot_calls} hot, {cold_calls} cold ({(100 * (hot_calls / total_calls))}% hot of total {total_calls})")
    return blueprint_number * best_geode_count
 
 
# Example Blueprint 1 and 2, Part 1
# assert solve_blueprint(24, 1, 4, 2, 3, 14, 2, 7) == 9  # 2s
# assert solve_blueprint(24, 2, 2, 3, 3, 8, 3, 12) == 24  # 15s
 
# Part 1 New Account - 100s
# assert solve_blueprint(24, 1, 4, 4, 4, 12, 3, 8) == 2 # 1
# assert solve_blueprint(24, 2, 2, 2, 2, 15, 2, 7) == 30 # 2
# assert solve_blueprint(24, 3, 4, 3, 4, 18, 4, 11) == 0 # 3
# assert solve_blueprint(24, 4, 2, 2, 2, 10, 2, 11) == 56 # 4
# assert solve_blueprint(24, 5, 3, 3, 2, 9, 2, 9) == 50 # 5
# assert solve_blueprint(24, 6, 3, 3, 2, 12, 2, 10) == 30 # 6
# assert solve_blueprint(24, 7, 4, 4, 4, 10, 2, 7) == 28 # 7
# assert solve_blueprint(24, 8, 4, 4, 2, 10, 3, 14) == 8 # 8
# assert solve_blueprint(24, 9, 3, 4, 3, 17, 3, 8) == 18 # 9
# assert solve_blueprint(24, 10, 3, 3, 3, 11, 2, 8) == 80 # 10
# assert solve_blueprint(24, 11, 4, 3, 3, 20, 2, 19) == 0 # 11
# assert solve_blueprint(24, 12, 3, 3, 3, 20, 2, 12) == 12 # 12
# assert solve_blueprint(24, 13, 3, 4, 4, 6, 2, 20) == 39 # 13
# assert solve_blueprint(24, 14, 4, 4, 3, 5, 3, 18) == 42 # 14
# assert solve_blueprint(24, 15, 3, 3, 4, 19, 4, 7) == 45 # 15
# assert solve_blueprint(24, 16, 3, 4, 4, 19, 4, 11) == 0 # 16
# assert solve_blueprint(24, 17, 2, 4, 3, 20, 2, 16) == 17 # 17
# assert solve_blueprint(24, 18, 3, 4, 4, 18, 3, 8) == 36 # 18
# assert solve_blueprint(24, 19, 3, 3, 2, 14, 3, 17) == 19 # 19
# assert solve_blueprint(24, 20, 2, 3, 3, 11, 3, 14) == 140 # 20
# assert solve_blueprint(24, 21, 3, 3, 3, 6, 2, 16) == 147 # 21
# assert solve_blueprint(24, 22, 2, 4, 4, 20, 3, 14) == 22 # 22
# assert solve_blueprint(24, 23, 4, 4, 3, 10, 2, 14) == 23 # 23
# assert solve_blueprint(24, 24, 4, 4, 2, 7, 4, 13) == 72 # 24
# assert solve_blueprint(24, 25, 3, 4, 4, 18, 4, 12) == 0 # 25
# assert solve_blueprint(24, 26, 4, 4, 4, 11, 4, 12) == 26 # 26
# assert solve_blueprint(24, 27, 4, 4, 4, 9, 4, 16) == 0 # 27
# assert solve_blueprint(24, 28, 4, 3, 3, 7, 2, 7) == 364 # 28
# assert solve_blueprint(24, 29, 4, 4, 2, 14, 4, 19) == 0 # 29
# assert solve_blueprint(24, 30, 4, 3, 4, 20, 2, 15) == 0 # 30
 
# Part 2 New Account
# assert solve_blueprint(32, 1, 4, 4, 4, 12, 3, 8) == 28  # 30s
# assert solve_blueprint(32, 2, 2, 2, 2, 15, 2, 7) == 158  # 50s
# assert solve_blueprint(32, 3, 4, 3, 4, 18, 4, 11) == 51  # 90s
 
# Example Blueprint 1 and 2, Part 2
# assert solve_blueprint(32, 1, 4, 2, 3, 14, 2, 7) == 56  # 40s
# assert solve_blueprint(32, 2, 2, 3, 3, 8, 3, 12) == 124 # FOREVER
 
# Part 2 Old Account
# assert solve_blueprint(32, 1, 3, 3, 3, 20, 2, 12) == 21
# assert solve_blueprint(32, 2, 2, 3, 3, 14, 3, 19) == 54
# assert solve_blueprint(32, 3, 4, 4, 2, 11, 2, 7) == 114
