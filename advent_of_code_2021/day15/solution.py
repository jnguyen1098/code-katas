#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *
from heapq import *

def increment(num, incr):
    return (num + incr - 1) % 9 + 1

def multiply_data(data):
    big_row = []
    for row in data:
        lol = []
        for i in range(5):
            tmp = row[:]
            for j in range(len(tmp)):
                tmp[j] = increment(tmp[j], i)
            for num in tmp:
                lol.append(num)
        big_row.append(lol)
    final = []
    for i in range(5):
        for _row in big_row:
            row = _row[:]
            for j in range(len(row)):
                row[j] = increment(row[j], i)
            final.append(row[:])
    return final

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
    expcts = [[40, 698], [315, 3022]]
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
