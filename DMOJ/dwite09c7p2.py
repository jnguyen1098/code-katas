#!/usr/bin/env python3

from functools import lru_cache
from math import sqrt

@lru_cache(None)
def is_prime(n):
    if n in [1, 2]:
        return True
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def get_primes(n):
    combine = 0
    for i in range(2, n + 1):
        if is_prime(i):
            combine += i
    print(combine)

for _ in range(5):
    get_primes(int(input()))
