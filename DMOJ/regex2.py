import re

N = int(input())

def censor(line):
    print(re.sub(r"\b[A-Za-z0-9]{4}\b", "****", line))

for _ in range(N):
    censor(input())
