#!/usr/bin/env python3.10

N = int(input())

count = 0

def generate(curr_number=["0"]):
    global count

    num = int("".join(curr_number))

    if num > N:
        return
    elif num != 0:
        count += 1

    curr_number.append("2")
    generate()
    curr_number.pop()

    curr_number.append("3")
    generate()
    curr_number.pop()

generate()

print(count)
