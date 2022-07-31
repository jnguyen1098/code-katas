line = input().split()

N, K = int(line[0]), int(line[1])

deer = []

for _ in range(N):
    deer.append(int(input()))

deer.sort()

count = 0
candy = K

for ru in deer:
    if candy < 1 or candy < ru:
        break
    candy -= ru
    count += 1

print(count)
