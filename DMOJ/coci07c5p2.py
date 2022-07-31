# f(13) = 12 because it's prime
import math
N = int(input())

limit = int(math.sqrt(N))

for i in range(2, limit + 1):
    if N % i == 0:
        print(N - (N // i))
        break
else:
    print(N - 1)  # prime
