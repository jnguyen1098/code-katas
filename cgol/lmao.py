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

def p(n, k):
    global calls

    coefficients = {0: 1}
    for iteration in range(1, k + 1):
        result = defaultdict(int)
        for weight in coefficients.keys():
            for term in range(n // iteration):
                calls += 1
                result[weight + iteration * term] += coefficients[weight]
        coefficients = result
    return coefficients[n - k]

for test, result in tests.items():
    n, k = test
    assert p(n, k) == result

print("Pass")
print(calls)
