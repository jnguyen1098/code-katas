import math

line = input().split()

N, P = int(line[0]), int(line[1])

scores = []

for _ in range(N):
    line = input().split()
    name = line[0]
    M = int(line[1])
    CS = int(line[2])
    E = int(line[3])
    score = (4 * math.sqrt(M)) + (3 * math.pow(CS, P)) - (4 * E)
    scores.append((score, name)) 

scores.sort()

print(scores[-1][1], math.floor(scores[-1][0]))
print(scores[0][1], math.floor(scores[0][0]))
