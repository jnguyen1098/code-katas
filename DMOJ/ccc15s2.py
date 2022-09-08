J = int(input())

A = int(input())

jerseys = []
athletes = []

for i in range(J):
    jerseys.append((i + 1, input()))

reqs = 0
jerseys = set(jerseys)

for _ in range(A):
    line = input().split()
    number, size = int(line[1]), line[0]

    if size == "L":
        if (number, "L") in jerseys:
            reqs += 1
            jerseys.remove((number, "L"))
    elif size == "M":
        if (number, "M") in jerseys:
            reqs += 1
            jerseys.remove((number, "M"))
        elif (number, "L") in jerseys:
            reqs += 1
            jerseys.remove((number, "L"))
    elif size == "S":
        if (number, "S") in jerseys:
            reqs += 1
            jerseys.remove((number, "S"))
        elif (number, "M") in jerseys:
            reqs += 1
            jerseys.remove((number, "M"))
        elif (number, "L") in jerseys:
            reqs += 1
            jerseys.remove((number, "L"))

print(reqs)
