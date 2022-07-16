N = int(input())

numbers = []

for i in range(N):
    numbers.append(int(input()))

for num in sorted(numbers):
    print(num)
