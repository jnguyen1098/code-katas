def is_mirror(line):
    return line in ["qp", "pq", "db", "bd"]

print("Ready")
while True:
    line = input()
    if line == "  ":
        break
    if is_mirror(line):
        print("Mirrored pair")
    else:
        print("Ordinary pair")
