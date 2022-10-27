N = int(input())

import math

lmao = 0

for i in range(1, N + 1):
    if N % i == 0:
        print("div", i)
        lmao += i

print(lmao)
