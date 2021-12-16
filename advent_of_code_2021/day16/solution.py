#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

def bin_to_int(bnum):
    return int(bnum, 2)

def parse_literal(stream, it, pad=False):
    bin_chunks = []
    while True:
        byte = stream[it : it + 5]
        if len(byte) < 5:
            break
        bin_chunks.append(byte[1:])
        it += 5 
        if byte[0] == "0":
            while pad and it != len(stream) and stream[it] == "0":
                it += 1 # TODO: lmao
            break
    value = bin_to_int("".join(bin_chunks))
    return value, it

def get_version(stream, it=0):
    return bin_to_int(stream[it:it+3])

class Packet:
    def __init__(self, stream):
        self.stream = stream
        self.version = bin_to_int(stream[0:3])
        self.typeid = bin_to_int(stream[3:6])
        self.value = -1

        self.versum = self.version
    
        # Literal
        if self.typeid == 4:
            self.value, it = parse_literal(stream, 6)
        # Operator
        else:
            # the next 15 bits are a number representing total length in bits of the subs
            if stream[6] == "0":
                bitlen = bin_to_int(stream[7 : 7 + 15])
                print(bitlen, "(0) bit length of the subs")
                it = 7 + 15
                while bitlen > 0:
                    consumed = 0
                    self.versum += get_version(stream, it)
                    value, new_it = parse_literal(stream, it + 6, pad=True)
                    print(stream[it : new_it - 1], value)
                    bitlen += (it - new_it + 1)
                    it = new_it - 1
            # the next 11 bits represent the number of sub-packets immediately following
            elif stream[6] == "1":
                subcnt = bin_to_int(stream[7 : 7 + 11])
                print(subcnt, "(1) number of subs")
                it = 7 + 11
                while subcnt:
                    self.versum += get_version(stream, it)
                    value, new_it = parse_literal(stream, it + 6, pad=False)
                    print(stream[it : new_it], value)
                    it = new_it
                    subcnt -= 1
            else:
                print(rev(red(f"fatal error: length type id is {stream[6]}")))
                exit()

    def __str__(self):
        return f"Version: {self.version}\n" +\
            f"Type ID: {self.typeid}\n" +\
            f"  Value: {self.value}\n" +\
            f" Stream: {self.stream}\n" +\
            f" Versum: {self.versum}\n"

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
        return 0
    elif prob == 2:
        return 0
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    # literal should be 6, 4, 2021
    # operator0 should be ver=1 type=6 lent=0 bits=27 literal=10 literal=20
    # operator1 should be ver=7 type=3 lent=1 lits=3 literal=1 literal=2 literal=3
    inputs = ["literalpacket", "operator0", "operator1", "real"]
    expcts = [[1, 1, 1, 1], [1, 1, 1, 1]]
    shortc = False

    for idx, part in enumerate(expcts):
        for filename, expected in zip(inputs, part):
            print(cya(rev(f"Filename: {filename}")))
            output = solve(idx + 1, filename)
            passed, msg = expect(output, expected)
            result = rev(grn("PASS") if passed else red("FAIL"))
            print(f"Part {idx + 1}: {output} {grn(msg) if passed else red(msg)}\n")
            if not passed and shortc: exit()
        print("\n" * 2)
