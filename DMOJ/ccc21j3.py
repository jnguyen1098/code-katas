
dir = None

while True:
    line = input()
    if line == "99999":
        break
    n1 = int(line[0])
    n2 = int(line[1])

    if (n1 + n2) % 2 == 1:
        dir = "left"
    elif (n1 + n2) % 2 == 0 and (n1 + n2) != 0:
        dir = "right"

    steps = line[2:]

    print(dir, steps)
