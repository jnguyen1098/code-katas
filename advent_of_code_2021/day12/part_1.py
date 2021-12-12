#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

class Container:
    def __init__(self):
        self.count = 0

def dfs(graph, key, seen, path, container):
    if key == "end":
        print("hit the end. final path", path)
        container.count += 1
        return container.count
    if not key.isupper():
        seen.add(key)
    for value in graph[key]:
        if value not in seen:
            path.append(value)
            dfs(graph, value, seen, path, container)
            path.pop()
            try:
                seen.remove(value)
            except:
                pass
    return container.count

def dfs2(graph, key, seen, path, container, vip):
    if key == "end":
        print("hit the end. final path", path)
        container.count += 1
        return container.count
    if not key.isupper():
        if key not in seen:
            seen[key] = 0
        seen[key] += 1
    for value in graph[key]:
        if value not in seen or seen[value] == 0:
            path.append(value)
            dfs2(graph, value, seen, path, container, vip)
            path.pop()
            try:
                seen[value] -= 1
                if seen[value] == 0:
                    seen.pop(value)
            except:
                pass
    return container.count

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(strsep(line, "-"))

    start = defaultdict(list)

    for left, right in lines:
        start[left].append(right)
        start[right].append(left)

    if prob == 1:
        return dfs(start, "start", set(), ["start"], Container())
    elif prob == 2:
        return dfs2(start, "start", {}, ["start"], Container(), None)
        """
        for key in start.keys():
            if key in ["start", "end"] or key.isupper(): continue
        return dfs2(start, "start", set(), ["start"], Container())
        """
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputs = ["small", "example", "real"]
    exp = [ [10, 36], [19, 40], [4970, 60], ]
    short_circuit_file = True

    for filename, expected in zip(inputs, exp):
        print(cya(rev(f"Filename: {filename}")))
        for tno in [1, 2]:
            output = solve(tno, filename)
            passed, msg = expect(output, expected[tno - 1])
            result = rev(grn("PASS") if passed else red("FAIL"))
            print(f"Part {tno}: {output} {grn(msg) if passed else red(msg)}")
            if not passed and short_circuit_file: exit()
        print("\n" * 2)
