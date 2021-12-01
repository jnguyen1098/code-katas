#!/usr/bin/env python3

from collections import deque

fin = open("input", "r").read().split()
depths = [int(line) for line in fin]
count = 0

window = deque([])
cum_sum = 0
windows = []

for depth in depths:
    window.append(depth)
    cum_sum += depth
    if len(window) == 3:
        windows.append(cum_sum)
        cum_sum -= window.popleft()

for i in range(1, len(windows)):
    if windows[i] > windows[i - 1]:
        count += 1

print(count)
