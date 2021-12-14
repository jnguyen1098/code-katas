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

    times = 10 if prob == 1 else 40

    from collections import Counter
    for i in range(times):
        print(i, len(template))
        i = 0
        while i < len(template) - 1:
            l, r = template[i], template[i + 1]
            pat = f"{l}{r}"
            template.insert(i + 1, recipes[pat])
            i += 1
            i += 1

    counter = Counter(template)
    listcnt = sorted([(freq, letter) for letter, freq in counter.items()])
    return int(listcnt.pop(-1)[0]) - int(listcnt.pop(0)[0])

    print(listcnt)
    print(recipes)

if __name__ == "__main__":
    inputs = ["example", "real"]
    expcts = [[1588, 2447], [50, 60]]
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
