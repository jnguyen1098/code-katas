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

    recipes = {}

    for line in lines:
        recipes[f"{line[0]}{line[1]}"] = line[2]

    tiles = defaultdict(int)
    freqs = Counter(template)

    for i in range(len(template) - 1):
        l, r = template[i], template[i + 1]
        tiles[f"{l}{r}"] += 1

    times = 10 if prob == 1 else 40

    def print_dict(my_dict):
        for key, value in my_dict.items():
            if value > 0:
                print(f"{key} = {value}")

    for i in range(times):
        reqs = copy.deepcopy(tiles)
        for key, value in reqs.items():
            tiles[key] -= value
            if tiles[key] == 0:
                tiles.pop(key)
            new = recipes[key]
            freqs[new] += value
            nl, nr = f"{key[0]}{new}", f"{new}{key[1]}"
            tiles[nl] += value
            tiles[nr] += value

    print("\ndone everything")
    print("letter frequencies", freqs)
    print("tile counts", tiles)
    counter = Counter(freqs)
    listcnt = sorted([(freq, letter) for letter, freq in counter.items()])
    return int(listcnt.pop(-1)[0]) - int(listcnt.pop(0)[0])

    print(listcnt)
    print(recipes)

if __name__ == "__main__":
    inputs = ["example", "real"]
    expcts = [[1588, 2447], [2188189693529, 60]]
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
