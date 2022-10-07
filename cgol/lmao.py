from collections import defaultdict

tests = {
    (8, 4): 5,
    (6, 3): 3,
    (7, 3): 4,
    (5, 2): 2,
    (6, 2): 3,
    (7, 2): 3,
    (8, 2): 4,
    (9, 2): 4,
    (10, 3): 8,
    (8, 4): 5,
    (12, 4): 15,
    (11, 3): 10,
    (4, 2): 2,
    (9, 3): 7,
    (9, 4): 6,
    (20, 1): 1,
    (70, 70): 1,
    (25, 8): 230,
    (70, 15): 284054,
    (99, 42): 613646,
    (120, 20): 97132873,
    (250, 130): 1844349560,
}

calls = 0

from functools import lru_cache

@lru_cache(None)
def fill(n, k):
    if n <= 0 or k <= 0:
        return 0
    if n == k:
        return 1
    return p(n - 1, k - 1) + p(n - k, k)

def p(n, k):
    print("global", n, k)
    table = []
    for i in range(n + 1):
        table.append([0] * (k + 1))

    for i in range(1, n + 1):
        table[i][1] = 1

    for i in range(1, k + 1):
        table[i][i] = 1

    for i in range(3, n + 1):
        for j in range(2, k + 1):
            if n < k:
                continue
            table[i][j] = table[i - 1][j - 1] + table[i - j][j]

    return table[n][k]

def p_(n, k):
    global calls
    target = n - k

    coefficients = {0: 1}
    for iteration in range(1, k + 1):
        result = defaultdict(int)
        for weight in coefficients.keys():
            if weight > target:
                break
            for term in range(n // iteration):
                if term * iteration + weight > target:
                    break
                calls += 1
                result[weight + iteration * term] += coefficients[weight]
        coefficients = result
    return coefficients[target]

for test, result in tests.items():
    n, k = test
    assert p(n, k) == result
    print(f"p({n}, {k}) pass")

print("Pass")
print(calls)
