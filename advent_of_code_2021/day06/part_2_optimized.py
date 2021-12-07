#!/usr/bin/env python3

from collections import defaultdict, Counter

def advance(data):
    thing = [0] * 9

    for i in range(9):
        thing[i] = data[(i + 1) % 9]

    thing[6] += data[0]
    return thing

tmp_data = [int(tmp) for tmp in open("input", "r").read().split(",")]

data = [0] * 9
for i in range(len(tmp_data)):
    data[tmp_data[i]] += 1

for i in range(256):
    data = advance(data)

print(sum(data))
print(sum(data) == 1686252324092)
