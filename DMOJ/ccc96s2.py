#!/usr/bin/env python3.10

N = int(input())

def solve(num):
    original_num = num
    while num > 99:
        print(num)
        popped = num % 10
        num //= 10
        num -= popped
    print(num)
    if num == 11:
        print(f"The number {original_num} is divisible by 11")
    else:
        print(f"The number {original_num} is not divisible by 11")
    print()


for _ in range(N):
    solve(int(input()))
