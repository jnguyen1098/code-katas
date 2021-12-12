#!/usr/bin/env python3

import json
import sys
sys.path.append("..")

from ansi import *
from comp import *

def dfs(graph, key, seen, path, counter):
    if key == "end":
        counter.data += 1
        return counter.data
    if not key.isupper():
        seen.add(key)
    for value in graph[key]:
        if value not in seen:
            path.append(value)
            dfs(graph, value, seen, path, counter)
            path.pop()
            try:
                seen.remove(value)
            except:
                pass
    return counter.data

def dfs2(graph, key, seen, path, counter, vip, paths):
    if key == "end":
        paths.add(str(json.dumps(path[:])))
        counter.data += 1
        return counter.data
    if not key.isupper():
        if key not in seen:
            seen[key] = 0
        seen[key] += 1
    for value in graph[key]:
        if value not in seen or seen[value] == 0 or (value == vip and seen[value] < 2):
            path.append(value)
            dfs2(graph, value, seen, path, counter, vip, paths)
            path.pop()
            try:
                seen[value] -= 1
                if seen[value] == 0:
                    seen.pop(value)
            except:
                pass
    return counter.data

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
        return dfs(start, "start", set(), ["start"], Pointer(0))
    elif prob == 2:
        count = 0
        seen = set()
        for key in start.keys():
            if key in ["start", "end"] or key.isupper(): continue
            tmp = dfs2(start, "start", {}, ["start"], Pointer(0), key, seen)
            count += tmp
        return len(seen)
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputs = ["small", "example", "real"]
    exp = [ [10, 36], [19, 103], [4970, 137948], ]
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
