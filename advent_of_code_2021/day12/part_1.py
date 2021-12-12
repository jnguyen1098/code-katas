#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def is_big(letter):
    return letter.isupper()

def dfs(graph, key, seen, path):
    print(key)
    seen.add(key)
    for value in graph[key]:
        if value not in seen:
            dfs(graph, value, seen, path)

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(strsep(line, "-"))

    start = defaultdict(list)

    for left, right in lines:
        start[left].append(right)

    dfs(start, "start", set(), [])

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputs = ["small", "example", "real"]
    exp = [ [10, 20], [30, 40], [50, 60], ]

    for filename, expected in zip(inputs, exp):
        print(cya(rev(f"Filename: {filename}")))
        for tno in [1, 2]:
            output = solve(tno, filename)
            passed, msg = expect(output, expected[tno - 1])
            result = rev(grn("PASS") if passed else red("FAIL"))
            print(f"Part {tno}: {output} {grn(msg) if passed else red(msg)}")
        print("\n" * 2)
