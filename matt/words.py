#!/usr/bin/env python3.10

import resource
import sys
import time

resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

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
    level += 1
    prindent(f"FAIL: assert that {message}: {expected=} {actual=}")
    level -= 1
    if FAILFAST:
        prindent(f"Failing fast")
        exit(1)

def read_all_words(filename):
    words = []
    with open(filename) as fp:
        for line in fp:
            words.append(line.strip())
    return words

def sign_word(word):
    result = 0
    for char in word:
        result |= ( 1 << (ord(char) - ord("a"))  )
    return result

def get_signatures(words):
    tuples = set()
    signatures = set()

    for word in words:
        if (signature := sign_word(word)) in signatures:
            continue
        signatures.add(signature)
        tuples.add((signature, word))

    return tuples

def unsign(signature):
    chars = []

    assert signature.bit_count() == 5

    for i in range(32):
        if (signature & (1 << i)):
            chars.append(chr(ord("a") + i))

    return "".join(chars)

def execute_query(filename):
    global level

    total_factor = 5

    num_words = total_factor
    word_length = total_factor
    uniques_per_word = word_length
    unique_chars_in_total = num_words * uniques_per_word

    words = read_all_words(filename)
    five_letter_words = [word for word in words if len(word) == word_length]
    signatures = []
    #signatures = sorted(list(get_signatures(five_letter_words)))
    #signatures = [tup for tup in signatures if tup[0].bit_count() == uniques_per_word]
    assert len(signatures) == 5977

    answer = 0


    return answer

def test_read_all_words_correct_length():
    global level
    level += 1
    prindent("Testing read_all_words()' length")

    words = read_all_words(FILENAME)
    assert_that("the right number of words is read", len(words), 370105)

    prindent("Done testing read_all_words()' length")
    level -= 1

def test_sign_word():
    global level
    level += 1
    prindent("Testing sign_word()")

    assert_that(
        "the word boob is signed correctly",
        sign_word("boob"),
        0b00000000000000000100000000000010,
    )

    prindent("Done testing sign_word()")
    level -= 1

def test_get_signatures():
    global level
    level += 1
    prindent("Testing get_signatures()")

    assert_that(
        "the set ['food', 'cat', 'oyster', 'ooooo'] is signed correctly",
        get_signatures(["food", "cat", "oyster", "ooooo"]),
        set([("dfoo", "food"), ("act", "cat"), ("eorsty", "oyster"), ("ooooo", "ooooo")]),
    )

    assert_that(
        "anagrams, once signed  in the same set, collide",
        get_signatures(["dfoo", "food", "doof"]),
        set([("dfoo", "dfoo")]),
    )

    prindent("Done testing get_signatures()")
    level -= 1

def test_correct_answer():
    global level
    level += 1
    prindent("Testing query execution")

    start = time.time()
    answer = execute_query(FILENAME)
    end = time.time()
    assert_that("the original answer in the video is given", answer, 538)

    prindent(f"Query executed in {end - start} seconds")

    prindent("Done testing query execution")
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
