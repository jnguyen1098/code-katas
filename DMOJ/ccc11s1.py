from collections import Counter

N = int(input())

lines = []

for _ in range(N):
    lines.append(input().casefold())

counter = Counter(" ".join(lines))

if counter["t"] > counter["s"]:
    print("English")
elif counter["t"] < counter["s"]:
    print("French")
else:
    print("French")
