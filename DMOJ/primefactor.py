#!/usr/bin/env python3

import math

N = int(input())

def factor(num):
    factors = []
    while num > 1:
        limit = int(math.sqrt(num))
        for i in range(2, limit + 1):
            if num % i == 0:
                factors.append(str(i))
                num //= i
                break
        else:
            factors.append(str(num))
            break
    print(" ".join(factors))

for _ in range(N):
    factor(int(input()))
