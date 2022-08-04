stream = input().split()

stack = []

def is_operator(char):
    return char in ["+", "-", "/", "*", "%", "^"]

def perform(l, op, r):
    l = float(l)
    r = float(r)
    if op == "+":
        return l + r
    if op == "-":
        return l - r
    if op == "/":
        return l / r
    if op == "*":
        return l * r
    if op == "%":
        return l % r
    if op == "^":
        return l ** r

for char in stream:
    if is_operator(char):
        r, l = stack.pop(), stack.pop()
        stack.append(perform(l, char, r))
    else:
        stack.append(char)

assert len(stack) == 1

print(stack.pop())
