N = int(input())

letters = {}

for _ in range(N):
    letter, prefix = input().split()
    letters[prefix] = letter

encoded = input()

l = 0
r = 0
result = []

while l < len(encoded):
    r += 1
    if (letter := letters.get(encoded[l : r])) is not None:
        result.append(letter)
        l = r

print("".join(result))
