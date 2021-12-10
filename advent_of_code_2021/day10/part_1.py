#!/usr/bin/env python3

inputname = "example"
inputname = "real"

inverse = { ")": "(", "]": "[", "}": "{", ">": "<" }
errorscore = { ")": 3, "]": 57, "}": 1197, ">": 25137 }

lines = open(inputname, "r").read().splitlines()

stack = []
score = 0

for idx, line in enumerate(lines):
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            popped = stack.pop()
            if popped != inverse[char]:
                score += errorscore[char]

print(score)
