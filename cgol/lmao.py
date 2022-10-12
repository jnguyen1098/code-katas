from collections import defaultdict
from functools import lru_cache

import random
import time

operations = 0


# TODO: implement the best ones in C
# TODO: add if k == 1 logic
# TODO: add cache check as a separate op than raw hit


def top_down(n, k):
    td_cache = defaultdict(dict)

    def go(n, k):
        global operations
        if (hit := td_cache[n].get(k)) is not None:
            return hit
        operations += 1
        if n <= 0 or k <= 0 or n < k:
            return 0
        if n == k:
            return 1
        td_cache[n][k] = go(n - 1, k - 1) + go(n - k, k)
        return td_cache[n][k]

    return go(n, k)

def top_down_stack(n, k):
    global operations
    td_cache = defaultdict(dict)

    stack = [(n, k)]

    while stack:
        n, k = stack.pop()
        if n <= 0 or k <= 0 or n < k:
            operations += 1
            td_cache[n][k] = 0
        elif n == k or k == 1:
            operations += 1
            td_cache[n][k] = 1
        else:
            repush = False
            stack.append((n, k))
            if k < n and (hit1 := td_cache[n - k].get(k)) is None:
                repush = True
                stack.append((n - k, k))
            if n > 1 and k > 1 and (hit2 := td_cache[n - 1].get(k - 1)) is None:
                repush = True
                stack.append((n - 1, k - 1))
            if repush:
                continue
            stack.pop()
            operations += 1
            td_cache[n][k] = hit1 + hit2

    return td_cache[n][k]

def top_down_array(n, k):
    td_cache = [] * (n + 1)
    for _ in range(n + 1):
        td_cache.append([-1] * (k + 1))

    def go(n, k):
        global operations
        if (hit := td_cache[n][k]) != -1:
            return hit
        operations += 1
        if n <= 0 or k <= 0 or n < k:
            return 0
        if n == k:
            return 1
        td_cache[n][k] = go(n - 1, k - 1) + go(n - k, k)
        return td_cache[n][k]

    return go(n, k)

def top_down_array_stack(n, k):
    global operations
    td_cache = [] * (n + 1)
    for _ in range(n + 1):
        td_cache.append([-1] * (k + 1))

    stack = [(n, k)]

    while stack:
        n, k = stack.pop()
        if n <= 0 or k <= 0 or n < k:
            operations += 1
            td_cache[n][k] = 0
        elif n == k or k == 1:
            operations += 1
            td_cache[n][k] = 1
        else:
            repush = False
            stack.append((n, k))
            if k < n and (hit1 := td_cache[n - k][k]) == -1:
                repush = True
                stack.append((n - k, k))
            if n > 1 and k > 1 and (hit2 := td_cache[n - 1][k - 1]) == -1:
                repush = True
                stack.append((n - 1, k - 1))
            if repush:
                continue
            stack.pop()
            operations += 1
            td_cache[n][k] = hit1 + hit2

    return td_cache[n][k]

def top_down_array_stack_1d(n, k):
    pass

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
        for test, expected in tests.items():
            n, k = test
            actual = p(n, k)
            assert actual == expected
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
        print(f"{name} done in {times[name]:.3f}s using {call_counts[name]} operations (ops per sec is {call_counts[name] / times[name]})")

trials = [
    Trial("         top down dp", top_down),
    Trial("        bottom up dp", bottom_up),
    Trial("      generator math", combinatorial),
    Trial("      top down stack", top_down_stack),
    Trial("      top down array", top_down_array),
    Trial("top down array stack", top_down_array_stack),
]

run_trials(trials, 100)
