#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

from collections import Counter

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        if line == "": break
        template = list(line)

    for line in gen:
        lines.append(parse(r"(\w)(\w) -> (\w)", line))

    recipes = {f"{line[0]}{line[1]}": line[2] for line in lines}

    tiles = defaultdict(int)
    freqs = Counter(template)

    for i in range(len(template) - 1):
        tiles[f"{template[i]}{template[i + 1]}"] += 1

    times = 10 if prob == 1 else 40

    for i in range(times):
        reqs = copy.deepcopy(tiles)
        for key, value in reqs.items():
            tiles[key] -= value
            result = recipes[key]
            freqs[result] += value
            tiles[f"{key[0]}{result}"] += value
            tiles[f"{result}{key[1]}"] += value

    return int(freqs.most_common()[0][1]) - int(freqs.most_common()[-1][1])

if __name__ == "__main__":
    inputs = ["example", "real"]
    expcts = [[1588, 2447], [2188189693529, 3018019237563]]
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
