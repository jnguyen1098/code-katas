#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_image_to_bin(self):
        self.assertEqual(image_to_bin("...#...#."), "000100010")

    def test_image_to_int(self):
        self.assertEqual(bin_to_int("000100010"), 34)

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 35)
        self.assertEqual(solve(1, "input"), 1)
        self.assertEqual(solve(2, "example"), 2)
        self.assertEqual(solve(2, "input"), 2)

if __name__ == "__main__":
    unittest.main()
