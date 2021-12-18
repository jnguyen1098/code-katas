#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_str_to_pair(self):
        self.assertEqual(str_to_pair("[1,2]"), [1, 2])
        self.assertEqual(str_to_pair("[1,[2,3]]"), [1, [2,3]])
        self.assertEqual(str_to_pair("[[4,[[[]]],6],[2,3]]"), [[4,[[[]]],6],[2,3]])

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
