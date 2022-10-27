num_routes = int(input())

smallest = 999999999

for _ in range(num_routes):
    test = sum(list(map(int, input().split()))[1:])
    smallest = min(test, smallest)

print(smallest)
