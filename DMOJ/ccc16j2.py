lines = []

for _ in range(4):
    lines.append(list(map(int, input().split())))

sums = set()

for row in lines:
    sums.add(sum(row))

for col in zip(lines):
    sums.add(sum(col[0]))

print("magic" if len(sums) == 1 else "not magic")
