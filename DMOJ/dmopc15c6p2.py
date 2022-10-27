import math

N = int(input())

deg = 0

for _ in range(N):
    amount = float(input())
    deg = math.fmod(deg + amount, 360)

print(f"{deg:.6f}")
