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

def get_first_zero(num):
    idx = 0
    while num & 1:
        num >>= 1
        idx += 1
    return idx

def get_first_empty_quintuplet(num):
    idxs = []
    idx = 0
    while num and len(idxs) < 5:
        if num & 1 == 0:
            idxs.append(idx)
        num >>= 1
        idx += 1
    while len(idxs) < 5:
        idxs.append(idx)
        idx += 1
    return idxs

def apply_mask(num, indices):
    for idx in indices:
        assert not num & (1 << idx)  # TODO remove this maybe
        num |= (1 << idx)
    return num

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
    signatures = sorted(list(get_signatures(five_letter_words)))
    signatures = [tup for tup in signatures if tup[0].bit_count() == uniques_per_word]

    if "alpha" in filename:  # lmao
        assert len(signatures) == 5977

    def backtrack(idx, words_left, mask):
        if words_left == 0:
            return 1
        if idx >= len(signatures):
            return 0
        answer = 0
        if (signatures[idx][0] & mask) == 0:
            answer += backtrack(idx + 1, words_left - 1, mask | signatures[idx][0])
        answer += backtrack(idx + 1, words_left, mask)
        return answer

    answer = 0

    answer += backtrack(0, 5, 0)

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
        set(
            [
                (0b00000000000000000100000000101000, "food"),
                (0b00000000000010000000000000000101, "cat"),
                (0b00000001000011100100000000010000, "oyster"),
                (0b00000000000000000100000000000000, "ooooo"),
            ]
        ),

    )

    assert_that(
        "anagrams, once signed  in the same set, collide",
        get_signatures(["dfoo", "food", "doof"]),
        set([(0b00000000000000000100000000101000, "dfoo")]),
    )

    prindent("Done testing get_signatures()")
    level -= 1

def test_get_first_zero():
    global level
    level += 1
    prindent("Testing get_first_zero()")

    assert_that(
        "full-zero has its first index returned",
        get_first_zero(0),
        0,
    )

    assert_that(
        "bitmask full of ones has its MSB+1 returned",
        get_first_zero(0b11111111111111111),
        17,
    )

    assert_that(
        "bitmask that is sparse and full of holes returns correct idx",
        get_first_zero(0b001100000011111011111),
        5,
    )

    prindent("Done testing get_first_zero()")
    level -= 1

def test_get_first_empty_quintuplet():
    global level
    level += 1
    prindent("Testing get_first_empty_quintuplet()")

    assert_that(
        "full-zero has its first 5 indices returned",
        get_first_empty_quintuplet(0),
        [0, 1, 2, 3, 4],
    )

    assert_that(
        "full-one has the first 5 indices following it returned",
        get_first_empty_quintuplet(0b11111),
        [5, 6, 7, 8, 9],
    )

    assert_that(
        "bitmask with a lot of holes returns the right answer",
        get_first_empty_quintuplet(0b0000000011110111011111),
        [5, 9, 14, 15, 16],
    )

    prindent("Done testing get_first_empty_quintuplet()")
    level -= 1

def test_apply_mask():
    global level
    level += 1
    prindent("Testing apply_mask()")

    assert_that(
        "apply_mask() works on the first four indices of full-zero",
        apply_mask(0, [0, 1, 2, 3]),
        0b1111,
    )

    assert_that(
        "apply_mask() works on random digits of full-zero",
        apply_mask(0, [5, 8, 13, 31]),
        0b10000000000000000010000100100000,
    )

    prindent("Done testing apply_mask()")
    level -= 1

def test_smoke_test():
    global level
    level += 1
    prindent("Running smoke test")

    start = time.time()
    answer = execute_query("words_smoke.txt")
    end = time.time()
    assert_that("a simpler correct answer is given", answer, 1)

    prindent(f"Query executed in {end - start} seconds")

    prindent("Done running smoke test")
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
    test_get_first_zero()
    test_get_first_empty_quintuplet()
    test_apply_mask()
    test_smoke_test()
    test_correct_answer()

    prindent("Done running all tests")
    level -= 1

if __name__ == "__main__":
    run_all_tests()
