N = int(input())

def misspell(string):
    idx, word = string.split()
    result = []
    for i in range(len(word)):
        if i == int(idx) - 1:
            continue
        result.append(word[i])
    print(idx, "".join(result))

print(N)
for _ in range(N):
    print(input())


#for _ in range(N):
#    misspell(input())
