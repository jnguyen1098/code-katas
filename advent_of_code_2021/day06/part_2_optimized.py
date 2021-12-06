#!/usr/bin/env python3

from collections import defaultdict, Counter

def advance(data):
    thing = defaultdict(int)
    thing[8] = data[0]
    thing[7] = data[8]
    thing[6] = data[7]
    for i in range(0, 7):
        thing[(i - 1) % 7] += data[i]
    return thing

data = Counter([int(tmp) for tmp in open("example", "r").read().split(",")])

for i in range(3):
    print(data)
    data = advance(data)

print(sum(data.values()))
print(sum(data.values()) == 1686252324092)
