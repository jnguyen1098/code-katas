N = int(input())

maze = []

for _ in range(N):
    maze.append(list(map(int, input().split())))

frontier = set([(0, 0)])
popped = set()

MOVES = ((-1, 0), (0, -1), (0, 1), (1, 0))

def get_move(x, y, dx, dy):
    if (x + dx >= 0 and x + dx < N) and (y + dy >= 0 and y + dy < N):
        return x + dx, y + dy
    return None

def get_moves(x, y):
    moves = []
    for dx, dy in MOVES:
        if (new_coord := get_move(x, y, dx, dy)) is not None:
            moves.append((new_coord[0], new_coord[1]))
    return moves

can_go = False

while len(frontier) > 0:
    x, y = frontier.pop()
    if (x, y) == (N - 1, N - 1):
        can_go = True
        break
    popped.add((x, y))
    moves = get_moves(x, y)
    for new_x, new_y in moves:
        if (new_x, new_y) not in frontier and (new_x, new_y) not in popped and maze[new_x][new_y] == 0:
            frontier.add((new_x, new_y))

print("yes" if can_go else "no")
