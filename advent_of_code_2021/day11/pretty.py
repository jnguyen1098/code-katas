#!/usr/bin/env python3

inputname = "real"

MOVES = ((-1, -1), (-1, 0), (-1, 1),
         (0, -1),           (0, 1),
         (1, -1),  (1, 0),  (1, 1))

_lines = open(inputname, "r").read().splitlines()
grid = [[int(char) for char in line] for line in _lines]

def add_to_all_cells(grid, rows, cols, amt):
    for i in range(rows):
        for j in range(cols):
            grid[i][j] += amt

def add_around_cell(grid, rows, cols, x, y, amt):
    for move in MOVES:
        new_x = x + move[0]
        new_y = y + move[1]
        if new_x >= 0 and new_x < rows and new_y >= 0 and new_y < cols:
            grid[new_x][new_y] += amt

def get_flash(grid, rows, cols):
    fls = set()
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] > 9:
                fls.add((i, j))
    return fls

def get_new_flash(grid, rows, cols, old_flash):
    new_fls = get_flash(grid, rows, cols)
    return new_fls - old_flash

def flash(grid, rows, cols, fls):
    for x, y in fls:
        add_around_cell(grid, rows, cols, x, y, 1)
        grid[x][y] = -math.inf

def clean_board(grid, rows, cols):
    cnt = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == -math.inf:
                grid[i][j] = 0
                cnt += 1
    return cnt

def advance_and_get_flashes(grid, rows, cols):
    add_to_all_cells(grid, rows, cols, 1)
    while fls := get_flash(grid, rows, cols):
        flash(grid, rows, cols, fls)
    return clean_board(grid, rows, cols)

total = 0
print_grid(grid)
for i in range(1000):
    total += advance_and_get_flashes(grid, len(grid), len(grid[0]))
    print_grid(grid)
print(total)
