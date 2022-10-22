#!/usr/bin/env python3.10

import time

FILENAME = "words_alpha.txt"
DEBUG = True
FAILFAST = True

level = 0

def prindent(message):
    if DEBUG:
        print("    " * level + message)

def assert_that(message, actual, expected):
    global level
    if actual == expected:
        return
    prindent(f"FAIL: assert that {message}: {expected=} {actual=}")
    if FAILFAST:
        prindent(f"Failing fast")
        exit(1)

def read_all_words(filename):
    words = []
    with open(filename) as fp:
        for line in fp:
            words.append(line)
    return words

def test_read_all_words_correct_length():
    global level
    level += 1
    words = read_all_words(FILENAME)
    assert_that("the right number of words is read", len(words), 370105)
    level -= 1

def run_all_tests():
    global level
    level += 1
    prindent("Running all tests")
    test_read_all_words_correct_length()
    prindent("Done running all tests")
    level -= 1

if __name__ == "__main__":
    run_all_tests()
