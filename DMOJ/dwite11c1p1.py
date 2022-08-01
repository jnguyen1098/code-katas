def number(token):
    for char in token:
        if char not in "0123456789":
            return False
    return True

def convert(token):
    if number(token):
        return token
    return token[::-1]

def telegraph(line):
    tokens = []
    for token in reversed(line.split()):
        tokens.append(convert(token))
    print(" ".join(tokens))

for _ in range(5):
    telegraph(input())
