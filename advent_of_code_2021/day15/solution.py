#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *
from heapq import *

def multiply_data(data):
    return [[]]

def solve(prob, inputname):

    data = []
    for line in yield_line(inputname):
        data.append(intgrid(line))

    if prob == 2:
        data = multiply_data(data)

    rows = len(data)
    cols = len(data[0])

    #         c   x  y      where c=cost
    queue = [(0, (0, 0))]

    seen = set()

    while queue:
        cost, popped = heappop(queue)
        if popped == (rows - 1, cols - 1):
            return cost
        for move in DIR.ADJA:
            if (successor := get_point(popped, move, rows, cols)) and successor not in seen:
                heappush(queue, (cost + data[successor[0]][successor[1]], successor))
                seen.add(successor)

    print("shouldnt be here lol")
    exit(1)

if __name__ == "__main__":
    inputs = ["example", "real"]
    expcts = [[40, 698], [315, 1]]
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
