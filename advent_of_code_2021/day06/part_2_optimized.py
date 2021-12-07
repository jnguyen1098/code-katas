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

"""
  thing[0] = data[1]
  thing[1] = data[2]
  thing[2] = data[3]
  thing[3] = data[4]
  thing[4] = data[5]
  thing[5] = data[6]
  thing[6] = data[7] + data[0]
  thing[7] = data[8]
  thing[8] = data[0]
"""
