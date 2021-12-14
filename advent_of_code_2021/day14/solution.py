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
    leftovers = defaultdict(int)
    letters = defaultdict(int)

    for letter in template:
        letters[letter] += 1

    for i in range(times):
        keys = Counter(list(counts.keys()))
        keys.update(leftovers)
        print(f"{i} = {sum(keys.values())}")
#        print("iterating over", list(counts.keys()), "and", leftovers[:], f"len {len(keys)}")
        leftovers.clear()

        for key, count in keys.items():
            pat = f"{key[0]}{key[1]}"
            counts[pat] -= count
            if counts[pat] < 1:
                counts.pop(pat)

        for key, count in keys.items():
            pat = f"{key[0]}{key[1]}"
            new = recipes[pat]
            nl, nr = f"{key[0]}{new}", f"{new}{key[1]}"
            for i in range(count):
#                print(f"tile: {pat} -> {new} : {nl} & {nr}")
    
                if nl in counts:
#                    print(f"duplicate {nl}. appending.")
                    leftovers[nl] += 1
                else:
                    counts[nl] = 1
                    
                    
                if nr in counts:
#                    print(f"duplicate {nr}. appending.")
                    leftovers[nr] += 1
                else:
                    counts[nr] = 1
    
            counts[nl] += count - 1
            counts[nr] += count - 1
#                print("adding", new)
            letters[new] += count

    print("fuck off", letters)
    print(counts)
    counter = Counter(letters)
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
