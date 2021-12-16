#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def bin_to_int(bnum):
    return int(bnum, 2)

def get(stream):
    for char in stream:
        yield char

def solve(prob, inputname):
    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(re.findall("\w\w", line)[:])

    _data = lines[0]
    _stream = []

    for datum in _data:
        _stream.append(format(int(datum, 16), "b").zfill(8))

    stream = "".join(_stream)

    print(stream)

    print(f"version is {stream[0:3]} or {bin_to_int(stream[0:3])}")
    print(f"typeid  is {stream[3:6]} or {bin_to_int(stream[3:6])}")

    it = 6
    while True:
        if len(stream[it : it + 5]) < 5:
            break
        print(stream[it : it + 5])
        it += 5 

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
    expcts = [[20, 30], [50, 60]]
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
