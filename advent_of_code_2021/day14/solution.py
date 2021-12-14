#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

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

    counts = defaultdict(int)

    for i in range(len(template) - 1):
        l, r = template[i], template[i + 1]
        counts[f"{l}{r}"] += 1

    times = 10 if prob == 1 else 40

    from collections import Counter
    leftovers = []
    for i in range(times):
        print(i, len(template))
        i = 0
        keys = list(counts.keys()) + leftovers[:]
        leftovers.clear()
        print("iterating over", keys)
        while keys:
            key = keys.pop(0)
            l, r = key[0], key[1]
            pat = f"{l}{r}"
            new = recipes[pat]
            nl, nr = f"{l}{new}", f"{new}{r}"
            counts[pat] -= 1
            if counts[pat] == 0:
                counts.pop(pat)
            if nl in counts:
                leftovers.append(nl)
            if nr in counts:
                leftovers.append(nr)
            counts[nl] += 1
            counts[nr] += 1

    print(counts)
    counter = Counter(counts)
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
