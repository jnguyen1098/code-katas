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

    def test_get_pair_from_idx(self):
        self.assertEqual(get_pair_from_idx(tokenize("[[1,9]"), 1, 5), [1, 9])
        self.assertEqual(get_pair_from_idx(tokenize("[[1,23]"), 1, 5), [1, 23])
        self.assertEqual(
            get_pair_from_idx(tokenize("[[[[0,7],4],[71,[[8,40]"), 16, 20), [8, 40]
        )

    def test_needs_to_explode(self):
        self.assertTrue(needs_to_explode(tokenize("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")))
        self.assertFalse(needs_to_explode(tokenize("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")))

    def test_explode(self):
        self.assertEqual(
            explode(tokenize("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")),
            tokenize("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")
        )
        self.assertEqual(
            explode(tokenize("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")),
            tokenize("[[[[0,7],4],[15,[0,13]]],[1,1]]")
        )
        self.assertEqual(
            explode(tokenize("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")),
            tokenize("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
        )

    def test_needs_to_split(self):
        self.assertTrue(needs_to_split(tokenize("[[[[0,7],4],[15,[0,13]]],[1,1]]")))
        self.assertFalse(needs_to_split(tokenize("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")))

    def test_get_split_idx(self):
        self.assertEqual(get_split_idx(tokenize("[[[[0,7],4],[15,[0,13]]],[1,1]]")), 13)

    def test_split_int(self):
        self.assertEqual(split_int(10), (5, 5))
        self.assertEqual(split_int(21), (10, 11))

    def test_split(self):
        self.assertEqual(
            split(tokenize("[[[[0,7],4],[15,[0,13]]],[1,1]]")),
            tokenize("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
        )
        self.assertEqual(
            split(tokenize("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")),
            tokenize("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")
        )

    def test_concat_tokens(self):
        self.assertEqual(
            concat_tokens(tokenize("[1,1]"), tokenize("[2,2]")),
            tokenize("[[1,1],[2,2]]")
        )
        self.assertEqual(
            concat_tokens(tokenize("[[[[4,3],4],4],[7,[[8,4],9]]]"), tokenize("[1,1]")),
            tokenize("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
        )

    def test_add_lines_basic(self):
        result = tokenize("[1,1]")
        result = add_lines(result, tokenize("[2,2]"))
        result = add_lines(result, tokenize("[3,3]"))
        result = add_lines(result, tokenize("[4,4]"))
        self.assertEqual(result, tokenize("[[[[1,1],[2,2]],[3,3]],[4,4]]"))

    def test_add_lines_harder(self):
        result = tokenize("[1,1]")
        result = add_lines(result, tokenize("[2,2]"))
        result = add_lines(result, tokenize("[3,3]"))
        result = add_lines(result, tokenize("[4,4]"))
        result = add_lines(result, tokenize("[5,5]"))
        self.assertEqual(result, tokenize("[[[[3,0],[5,3]],[4,4]],[5,5]]"))

    def test_insane(self):
        result = tokenize("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]")
        result = add_lines(result, tokenize("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]"))
        result = add_lines(result, tokenize("[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]"))
        result = add_lines(result, tokenize("[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]"))
        result = add_lines(result, tokenize("[7,[5,[[3,8],[1,4]]]]"))
        result = add_lines(result, tokenize("[[2,[2,2]],[8,[8,1]]]"))
        result = add_lines(result, tokenize("[2,9]"))
        result = add_lines(result, tokenize("[1,[[[9,3],9],[[9,0],[0,7]]]]"))
        result = add_lines(result, tokenize("[[[5,[7,4]],7],1]"))
        result = add_lines(result, tokenize("[[[[4,2],2],6],[8,7]]"))
        self.assertEqual(
            result, tokenize("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
        )

    def test_pipeline(self):
        list_of_token_lists = [
            tokenize("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]"),
            tokenize("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]"),
            tokenize("[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]"),
            tokenize("[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]"),
            tokenize("[7,[5,[[3,8],[1,4]]]]"),
            tokenize("[[2,[2,2]],[8,[8,1]]]"),
            tokenize("[2,9]"),
            tokenize("[1,[[[9,3],9],[[9,0],[0,7]]]]"),
            tokenize("[[[5,[7,4]],7],1]"),
            tokenize("[[[[4,2],2],6],[8,7]]"),
        ]
        self.assertEqual(
            pipeline(list_of_token_lists),
			tokenize("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
        )

    def test_get_magnitude(self):
        self.assertEqual(get_magnitude(tokenize("[9,1]"), 0, 4), 29)
        self.assertEqual(get_magnitude(tokenize("[1,9]"), 0, 4), 21)

if __name__ == "__main__":
    unittest.main()
