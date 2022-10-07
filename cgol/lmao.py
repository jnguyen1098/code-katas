from collections import defaultdict
from functools import lru_cache

import random
import time

operations = 0


def top_down(n, k):
    td_cache = defaultdict(dict)

    def go(n, k):
        if (hit := td_cache[n].get(k)) is not None:
            return hit
        global operations
        operations += 1
        if n <= 0 or k <= 0:
            return 0
        if n == k:
            return 1
        td_cache[n][k] = go(n - 1, k - 1) + go(n - k, k)
        return td_cache[n][k]

    return go(n, k)

def bottom_up(n, k):
    global operations

    table = []
    for i in range(n + 1):
        table.append([0] * (k + 1))

    for i in range(1, n + 1):
        table[i][1] = 1

    for i in range(1, k + 1):
        table[i][i] = 1

    for i in range(3, n + 1):
        for j in range(2, k + 1):
            operations += 1
            table[i][j] = table[i - 1][j - 1] + table[i - j][j]

    return table[n][k]

def combinatorial(n, k):
    global operations
    target = n - k

    coefficients = {0: 1}
    for iteration in range(1, k + 1):
        result = defaultdict(int)
        for weight in coefficients.keys():
            if weight > target:
                break
            for term in range(n // iteration):
                if term * iteration + weight > target:
                    break
                operations += 1
                result[weight + iteration * term] += coefficients[weight]
        coefficients = result
    return coefficients[target]

tests = {
    (8, 4): 5,
    (6, 3): 3,
    (7, 3): 4,
    (5, 2): 2,
    (6, 2): 3,
    (7, 2): 3,
    (8, 2): 4,
    (9, 2): 4,
    (10, 3): 8,
    (8, 4): 5,
    (12, 4): 15,
    (11, 3): 10,
    (4, 2): 2,
    (9, 3): 7,
    (9, 4): 6,
    (20, 1): 1,
    (70, 70): 1,
    (25, 8): 230,
    (70, 15): 284054,
    (99, 42): 613646,
    (120, 20): 97132873,
    (250, 130): 1844349560,
}

def test_runner(name, p, iterations):
    global operations
    operations = 0
    start = time.time()
    for _ in range(iterations):
        for test, result in tests.items():
            n, k = test
            assert p(n, k) == result
    end = time.time()
    return operations, end - start

class Trial:
    def __init__(self, name, runner):
        self.name = name
        self.runner = runner

def run_trials(trials, iterations):
    call_counts = defaultdict(int)
    times = defaultdict(float)

    for _ in range(iterations):
        random.shuffle(trials)
        for trial in trials:
            call_count, time = test_runner(trial.name, trial.runner, 1)
            call_counts[trial.name] += call_count
            times[trial.name] += time

    for name in sorted([trial.name for trial in trials]):
        print(f"{name} completed in {times[name]:.3f}s using {call_counts[name]} operations")

trials = [
    Trial("   top down dp", top_down),
    Trial("  bottom up dp", bottom_up),
    Trial("generator math", combinatorial),
]

run_trials(trials, 100)

# TODO intersperse iterations?
