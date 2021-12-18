#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_get_pair(self):
        self.assertEqual(get_pair("[1,2]"), [1, 2])
        self.assertEqual(get_pair("[1,[2,3]]"), [1, [2,3]])
        self.assertEqual(get_pair("[[4,[[[]]],6],[2,3]]"), [[4,[[[]]],6],[2,3]])

    def test_peek(self):
        self.assertIsNone(peek("hello", 4))
        self.assertEqual(peek("hello", 3), "o")
        self.assertEqual(peek("hello", 0), "e")

    def test_tokenize(self):
        self.assertEqual(tokenize("["), ["["])
        self.assertEqual(tokenize("]"), ["]"])
        self.assertEqual(tokenize(","), [","])
        self.assertEqual(tokenize("[,]"), ["[", ",", "]"])
        self.assertEqual(tokenize("[3]"), ["[", 3, "]"])
        self.assertEqual(tokenize("  [ 3 ]  "), ["[", 3, "]"])
        self.assertEqual(tokenize("[3,4]"), ["[", 3, ",", 4, "]"])
        self.assertEqual(tokenize("[303,434]"), ["[", 303, ",", 434, "]"])
        self.assertEqual(tokenize("[0,0]"), ["[", 0, ",", 0, "]"])

    def test_get_explode_idxs(self):
        self.assertEqual(get_explode_idxs("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"), (4, 8))
        self.assertEqual(get_explode_idxs("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"), (16, 20))
        self.assertEqual(get_explode_idxs("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"), (22, 26))

    def test_remove_token(self):
        self.assertEqual(remove_token(tokenize("[3,4]"), 0), tokenize("3,4]"))
        self.assertEqual(remove_token(tokenize("[3,4]"), 1), tokenize("[,4]"))
        self.assertEqual(remove_token(tokenize("[3,4]"), 2), ["[", 3, 4, "]"])
        self.assertEqual(remove_token(tokenize("[3,4]"), 3), tokenize("[3,]"))
        self.assertEqual(remove_token(tokenize("[3,4]"), 4), tokenize("[3,4"))

    def test_remove_range(self):
        self.assertEqual(remove_range(tokenize("[1,2,3]"), 0, 6), [])
        self.assertEqual(remove_range(tokenize("[1,2,3]"), 0, 0), tokenize("1,2,3]"))
        self.assertEqual(remove_range(tokenize("[1,2,3]"), 6, 6), tokenize("[1,2,3"))
        self.assertEqual(remove_range(tokenize("[1,2,3]"), 2, 4), ["[", 1, 3, "]"])

    def test_replace_range(self):
        test = tokenize("[1,2,3]")
        self.assertEqual(replace_range(test, 0, 6, "LMAO"), ["LMAO"])
        self.assertEqual(replace_range(test, 0, 0, "LMAO"), ["LMAO", 1, ",", 2, ",", 3, "]"])
        self.assertEqual(replace_range(test, 0, 1, "LMAO"), ["LMAO", ",", 2, ",", 3, "]"])
        self.assertEqual(replace_range(test, 6, 6, "LMAO"), ["[", 1, ",", 2, ",", 3, "LMAO"])
        self.assertEqual(replace_range(test, 5, 6, "LMAO"), ["[", 1, ",", 2, ",", "LMAO"])

    def test_first_left_num(self):
        self.assertIsNone(
            get_first_left_num(
                tokenize("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"), 5
            )
        )
        self.assertEqual(
            get_first_left_num(
                tokenize("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"), 6
            ), 5
        )

    def test_first_right_num(self):
        self.assertIsNone(
            get_first_right_num(
                tokenize("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"), 30
            )
        )
        self.assertEqual(
            get_first_right_num(
                tokenize("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"), 19
            ), 22
        )

    def test_needs_to_explode(self):
        self.assertTrue(needs_to_explode(tokenize("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")))
        self.assertFalse(needs_to_explode(tokenize("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")))

    def test_get_pair_from_idx(self):
        self.assertEqual(get_pair_from_idx(tokenize("[[1,9]"), 1, 5), [1, 9])
        self.assertEqual(get_pair_from_idx(tokenize("[[1,23]"), 1, 5), [1, 23])
        self.assertEqual(
            get_pair_from_idx(tokenize("[[[[0,7],4],[71,[[8,40]"), 16, 20), [8, 40]
        )

    def test_explode(self):
        self.assertEqual(
            explode(tokenize("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")),
            tokenize("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")
        )

    def test_snailnum_init_all_ints(self):
        test = SnailNum(1, 2)
        self.assertEqual(test.l, 1)
        self.assertEqual(test.r, 2)

    def test_snailnum_init_all_snail(self):
        snail1 = SnailNum(1, 2)
        snail1_copy = SnailNum(1, 2)
        snail2 = SnailNum(3, 4)
        snail2_copy = SnailNum(3, 4)
        test = SnailNum(snail1, snail2)
        self.assertEqual(test.l, snail1_copy)
        self.assertEqual(test.r, snail2_copy)

if __name__ == "__main__":
    unittest.main()
