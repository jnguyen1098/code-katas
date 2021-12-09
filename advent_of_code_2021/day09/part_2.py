#!/usr/bin/env python3

from collections import deque

MOVES = ((-1, 0), (0, -1), (0, 1), (1, 0))

def is_low_point(point, x, y, rows, cols):
    for MOVE in MOVES:
        new_x = x + MOVE[0]
        new_y = y + MOVE[1]
        if new_x >= 0 and new_x < rows and new_y >= 0 and new_y < cols:
            if point[x][y] >= point[new_x][new_y]:
                return False
    return True

def get_basin_size(point, x, y, rows, cols):
    bfs = deque([(x, y)])
    size = 1
    pushed = []
    for i in range(rows):
        pushed.append([0] * cols)

    while bfs:
        pop_x, pop_y = bfs.popleft()
        curr_val = point[pop_x][pop_y]
        point[pop_x][pop_y] = 9
        for MOVE in MOVES:
            new_x = pop_x + MOVE[0]
            new_y = pop_y + MOVE[1]
            if new_x >= 0 and new_x < rows and new_y >= 0 and new_y < cols:
                if pushed[new_x][new_y]:
                    continue
                if point[new_x][new_y] != 9 and point[new_x][new_y] >= curr_val:
                    size += 1
                    bfs.append((new_x, new_y))
                    pushed[new_x][new_y] = 1

    return size

def mult_basin(filename):
    _lines = open(filename, "r").read().splitlines()
    lines = [list(map(int, row)) for row in _lines]
    basins = []

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if is_low_point(lines, i, j, len(lines), len(lines[0])):
                basins.append(get_basin_size(lines, i, j, len(lines), len(lines[0])))

    basins.sort()
    result = basins.pop() * basins.pop() * basins.pop()
    return result

tests = (
    ("example", 1134),
    ("real", 950600),
)

for idx, test in enumerate(tests):
    res = mult_basin(test[0])
    if res != test[1]:
        print(f"Failed test {idx}")
        exit()
    print(f"Passed test {idx}")

print("Passed all tests")
