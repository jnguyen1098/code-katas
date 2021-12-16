#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def bin_to_int(bnum):
    return int(bnum, 2)

class Packet:
    def __init__(self, stream):
        self.stream = stream
        self.version = bin_to_int(stream[0:3])
        self.typeid = bin_to_int(stream[3:6])
    
        it = 6
        bin_chunks = []
        while True:
            byte = stream[it : it + 5]
            if len(byte) < 5:
                break
            bin_chunks.append(byte[1:])
            it += 5 
            if byte[0] == "0":
                while it != len(stream) and stream[it] == "0":
                    it += 1
                break

        self.value = bin_to_int("".join(bin_chunks))

    def __str__(self):
        return f"Version: {self.version}\n" +\
            f"Type ID: {self.typeid}\n" +\
            f"  Value: {self.value}\n" +\
            f" Stream: {self.stream}\n"

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

    packet = Packet(stream)
    print(packet)

    if prob == 1:
        return 1
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    inputs = ["literalpacket", "real"]
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
