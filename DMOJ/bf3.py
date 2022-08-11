#!/usr/bin/env python3

import math

N = int(input())

def is_prime(candidate):
    if candidate == 1: return False
    limit = int(math.sqrt(candidate))
    for i in range(2, limit + 1):
        if candidate % i == 0:
            return False
    return True

candidate = N
while True:
    if is_prime(candidate):
        print(candidate)
        break
    candidate += 1
