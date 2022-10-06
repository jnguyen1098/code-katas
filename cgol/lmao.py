from collections import defaultdict

n = 120
k = 20


xd = 0

def mult(poly, order):
    global xd
    result = defaultdict(int)
    for i in poly.keys():
        for j in range(n):
            xd = max(xd, i + j)
            result[i + j] += poly[i] * (1 if j % order == 0 else 0)
    return result

start = {0: 1}
for i in range(1, k + 1):
    start = mult(start, i)

print(xd)

print(f"p({n}, {k}) = {start[n - k]}")

assert start[n - k] == 97132873

print("GOOD")
