#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(intgrid(line))

    rows = len(lines)
    cols = len(lines[0])

    MOVES = ((-1, 0), (0, 1), (1, 0), (0, -1))

    import networkx as nx
    G = nx.Graph()

    for i in range(rows):
        for j in range(cols):
            for move in MOVES:
                if new_point := get_point((i, j), move, rows, cols):
                    G.add_edge(f"{i},{j}", f"{new_point[0]},{new_point[1]}")
                    G[f"{i},{j}"][f"{new_point[0]},{new_point[1]}"]["weight"] = lines[int(new_point[0])][int(new_point[1])]

    path = nx.shortest_path(G, "0,0", f"{rows-1},{cols-1}", weight="weight")

    tot = 0
    for node in path:
        spl = node.split(",")
        print(spl[0], spl[1])
        tot += lines[int(spl[0])][int(spl[1])]
    print(tot)

    exit()

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputs = ["example", "real"]
    expcts = [[40, 30], [50, 60]]
    shortc = True

    for idx, part in enumerate(expcts):
        for filename, expected in zip(inputs, part):
            print(cya(rev(f"Filename: {filename}")))
            output = solve(idx + 1, filename)
            passed, msg = expect(output, expected)
            result = rev(grn("PASS") if passed else red("FAIL"))
            print(f"Part {idx + 1}: {output} {grn(msg) if passed else red(msg)}\n")
            if not passed and shortc: exit()
        print("\n" * 2)
"""
class Solution:
    def minPathSum(self, lines: List[List[int]]) -> int:
        
        rows = len(lines)
        cols = len(lines[0])
        
        for i in range(1, cols):
            lines[0][i] += lines[0][i - 1]
        
        for i in range(1, rows):
            lines[i][0] += lines[i - 1][0]
        
        for i in range(1, rows):
            for j in range(1, cols):
                lines[i][j] += min(lines[i - 1][j], lines[i][j - 1])
        
        return lines[rows - 1][cols - 1]
"""
