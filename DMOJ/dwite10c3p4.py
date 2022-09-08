#!/usr/bin/env python3.10


boards = []

try:
    while True:
        tmp_board = []
        while (line := input()) != "-" * 10:
            tmp_board.append(list(line))
        else:
            boards.append(tmp_board)
except:
    pass

def still_trees_left(board):
    for row in board:
        for char in row:
            if char == "T":
                return True
    return False

def serialize_board(board):
    return "".join(["".join(row) for row in board])

ADJACENT = (
    (-1, 0),
    (0, -1),
    (0, 1),
    (1, 0),
)

def step(board):
    burning_trees = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "F":
                burning_trees.add((i, j))
    for x, y in burning_trees:
        for dx, dy in ADJACENT:
            new_x = x + dx
            new_y = y + dy
            if (new_x >= 0 and new_x < 10) and (new_y >= 0 and new_y < 10):
                if board[new_x][new_y] == "T":
                    board[new_x][new_y] = "F"

def get_count(board):
    turns = 0

    last_serialized_board = None
    while still_trees_left(board):
        if (curr_board_serial := serialize_board(board)) == last_serialized_board:
            break
        step(board)
        turns += 1
        last_serialized_board = curr_board_serial

    return turns if not still_trees_left(board) else -1

for board in boards:
    print(get_count(board))
