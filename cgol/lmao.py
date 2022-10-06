from collections import defaultdict

n = 250
k = 130

def mult(poly, order):
    result = defaultdict(int)
    for i in poly.keys():
        for j in range(n):
            if j * order > n:
                break
            result[i + order * j] += poly[i]
    return result

start = {0: 1}
for i in range(1, k + 1):
    start = mult(start, i)

print(f"p({n}, {k}) = {start[n - k]}")

assert start[n - k] == 1844349560

print("GOOD")
