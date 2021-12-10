#!/usr/bin/env python3

inputname = "example"
inputname = "real"

inverse = { ")": "(", "]": "[", "}": "{", ">": "<" }
errorscore = { "(": 1, "[": 2, "{": 3, "<": 4 }

lines = open(inputname, "r").read().splitlines()

newlines = []

for idx, line in enumerate(lines):
    stack = []
    bad = False
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            popped = stack.pop()
            if popped != inverse[char]:
                bad = True
    if not bad:
        newlines.append(line)

scores = []
for line in newlines:
    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            popped = stack.pop()
    score = 0
    while stack:
        score = score * 5 + errorscore[stack.pop()]
    scores.append(score)

print(sorted(scores)[len(scores) // 2])
