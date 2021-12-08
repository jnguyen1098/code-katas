#!/usr/bin/env python3

import math

"""
letters = {
    1: "cf",
    7: "acf",
    4: "bcdf",
    2: "acdeg",
    3: "acdfg",
    5: "abdfg",
    0: "abcefg",
    6: "abdefg",
    9: "abcdfg",
    8: "abcdefg",
}

digit = {
    "cf": 1,
    "acf": 7,
    "bcdf": 4,
    "acdeg": 2,
    "acdfg": 3,
    "abdfg": 5,
    "abcefg": 0,
    "abdefg": 6,
    "abcdfg": 9,
    "abcdefg": 8,
}
"""

def print_map(translate):
    for letter in "abcdefg":
        result = translate.get(letter)
        print(f"{letter}: {result}")
    print()

def deduce_a(letters, models):
    two = None
    three = None
    for model in models:
        if len(model) == 2:
            two = set(model)
        if len(model) == 3:
            three = set(model)
    if not all([two, three]):
        print("could not find both 2 and 3")
        exit(1)
    letters["a"] = (three - two).pop()

strings = set([
    "cf",
    "acf",
    "bcdf",
    "acdeg",
    "acdfg",
    "abdfg",
    "abcefg",
    "abdefg",
    "abcdfg",
    "abcdefg",
])

digit = {
    "cf": 1,
    "acf": 7,
    "bcdf": 4,
    "acdeg": 2,
    "acdfg": 3,
    "abdfg": 5,
    "abcefg": 0,
    "abdefg": 6,
    "abcdfg": 9,
    "abcdefg": 8,
}

inputname = "small"
inputname = "example"

lines = open(inputname, "r").read().splitlines()

finale = 0

for idx, line in enumerate(lines):
    letters = {}
    model_line, test_line = line.split(" | ")
    models = ["".join(sorted(word)) for word in model_line.split()]
    tests = ["".join(sorted(word)) for word in test_line.split()]
    print(f"{' '.join(models)} | {' '.join(tests)}")

    import itertools
    for perm in itertools.permutations("abcdefg"):
        test = {}
        tmp_models = []
        tmp_tests = []
        for i in range(len(perm)):
            test[perm[i]] = list("abcdefg")[i]
        for idx, model in enumerate(models):
            test_model = list(model)
            for i in range(len(test_model)):
                test_model[i] = test[test_model[i]]
            tmp_models.append("".join(sorted(test_model[:])))
        for idx, _test in enumerate(tests):
            test_test = list(_test)
            for i in range(len(test_test)):
                test_test[i] = test[test_test[i]]
            tmp_tests.append("".join(sorted(test_test[:])))
        if set(tmp_models) == strings:
            tmp = []
            for test in tmp_tests:
                tmp.append(str(digit[test]))
            cnt = int("".join(tmp))
            print(cnt)
            finale += cnt
            break

print(finale)
