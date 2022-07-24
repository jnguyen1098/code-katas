board = []

for _ in range(10):
    board.append(list(input().split()))
"""
with open("input.txt") as fp:
    for line in (lines := fp.readlines()):
        board.append(line.split())
"""

def is_numeric(x, y):
    for char in board[x][y]:
        if not char.isdigit():
            return False
    return True

def test_is_numeric():
    yes_it_is = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0)
    ]
    for x, y in yes_it_is:
        assert is_numeric(x, y)
    no_its_not = [
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (0, 7),
        (0, 8),
    ]

num_rows = 10
num_cols = 9

def solved(x, y):
    if is_numeric(x, y):
        return True
    if board[x][y] == "*":
        return True
    return False

def test_solved():
    assert solved(0, 0)
    assert not solved(0, 3)
    assert solved(8, 8)
    assert not solved(0, 8)

def get_components(x, y):
    return board[x][y].split("+")

def test_get_components():
    assert get_components(0, 0) == ["1"]
    assert get_components(0, 3) == ["A1", "A2", "A3"]
    assert get_components(1, 1) == ["0"]

def component_to_coords(component):
    x = ord(component[0]) - 65
    y = int(component[1:]) - 1
    return x, y

def test_component_to_coords():
    assert component_to_coords("A1") == (0, 0)
    assert component_to_coords("F8") == (5, 7)

def solve(x, y, seen):
    if board[x][y] == "*":
        return "*"

    if is_numeric(x, y):
        return board[x][y]

    if (x, y) in seen:
        board[x][y] = "*"
        return "*"

    seen.add((x, y))

    value = 0
    components = get_components(x, y)

    for component in components:
        if component == "*":
            board[x][y] = "*"
            return "*"
        n_x, n_y = component_to_coords(component)
        if solve(n_x, n_y, seen) == "*":
            board[x][y] = "*"
            return "*"
        value += int(solve(n_x, n_y, seen))

    board[x][y] = str(value)
    return str(value)

def test_solve():
    assert solve(0, 0, set()) == "1"
    assert solve(0, 1, set()) == "2"
    assert solve(0, 5, set()) == "16"
    assert solve(0, 6, set()) == "*"

if __name__ == "__main__":
    for i in range(num_rows):
        for j in range(num_cols):
            if not solved(i, j):
                solve(i, j, set())
    for row in board:
        print(" ".join(row))
