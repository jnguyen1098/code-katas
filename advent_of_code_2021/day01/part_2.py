#!/usr/bin/env python3

fin = open("input", "r").read().split()
lines = [line for line in fin]
count = 0
for i in range(1, len(lines)):
    if int(lines[i]) > int(lines[i - 1]):
        count += 1
print(count)
