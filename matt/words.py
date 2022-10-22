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

def sign_word(word):
    return "".join(sorted(list(word)))

def get_signatures(words):
    signatures = set()

    for word in words:
        signatures.add((sign_word(word), word))

    return signatures

def execute_query(filename):
    answer = 0

    words = read_all_words(filename)
    five_letter_words = [word for word in words if len(word) == 5]
    signatures = get_signatures(five_letter_words)

    return answer

def test_read_all_words_correct_length():
    global level
    level += 1
    words = read_all_words(FILENAME)
    assert_that("the right number of words is read", len(words), 370105)
    level -= 1

def test_sign_word():
    global level
    level += 1

    assert_that(
        "the word boob is signed correctly",
        sign_word("boob"),
        "bboo"
    )

    level -= 1

def test_get_signatures():
    global level
    level += 1

    assert_that(
        "the set ['food', 'cat', 'oyster', 'ooooo'] is signed correctly",
        get_signatures(["food", "cat", "oyster", "ooooo"]),
        set([("dfoo", "food"), ("act", "cat"), ("eorsty", "oyster"), ("ooooo", "ooooo")])
    )


    level -= 1

def test_correct_answer():
    global level
    level += 1

    start = time.time()
    answer = execute_query(FILENAME)
    end = time.time()
    assert_that("the original answer in the video is given", answer, 538)

    prindent(f"Query executed in {end - start} seconds")

    level -= 1

def run_all_tests():
    global level
    level += 1
    prindent("Running all tests")

    test_read_all_words_correct_length()
    test_sign_word()
    test_get_signatures()
    test_correct_answer()

    prindent("Done running all tests")
    level -= 1

if __name__ == "__main__":
    run_all_tests()
