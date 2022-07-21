#!/usr/bin/env python3.10

BOARD_COUNT = 2

boards = []

for _ in range(BOARD_COUNT):
    tmp_board = []
    while (line := input()) != "-" * 10:
        tmp_board.append(list(line))
    else:
        boards.append(tmp_board)

def still_trees_left(board):
    for row in board:
        for char in row:
            if char == "T":
                return True
    return False

def serialize_board(board):
    return "".join(["".join(row) for row in board])

def step(board):
    pass

def get_count(board):
    turns = 0

    last_serialized_board = serialize_board(board)
    while still_trees_left(board):
        curr_board_serial = serialize_board(board)
        if last_serialized_board == curr_board_serial:
            break
        step(board)
        turns += 1
        last_serialized_board = serialize_board(board)

    return turns

for board in boards:
    print(get_count(board))
