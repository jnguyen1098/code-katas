#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_image_to_bin(self):
        self.assertEqual(image_to_bin("...#...#."), "000100010")

    def test_image_to_int(self):
        self.assertEqual(bin_to_int("000100010"), 34)

    def test_image_to_int(self):
        self.assertEqual(image_to_int("...#...#."), 34)

    def test_binmask(self):
        self.assertEqual(count(
            [
                "#..#.",
                "#....",
                "##..#",
                "..#..",
                "..###",
            ], 2, 2, 5, 5
        ), 34)

    def test_relevant(self):
        image = [
            "..........",
            "..........",
            "..........",
            "..######..",
            "..#....#..",
            "..#....#..",
            "..######..",
            "..........",
            "..........",
            "..........",
        ]
        for i in range(1, 9):
            self.assertTrue(relevant(image, 2, i, 10, 10))
            self.assertTrue(relevant(image, 7, i, 10, 10))

        for i in range(1, 9):
            self.assertFalse(relevant(image, 1, i, 10, 10))
            self.assertFalse(relevant(image, 8, i, 10, 10))

        for i in range(2, 8):
            self.assertTrue(relevant(image, i, 1, 10, 10))
            self.assertTrue(relevant(image, i, 8, 10, 10))

        for i in range(2, 8):
            self.assertFalse(relevant(image, i, 0, 10, 10))
            self.assertFalse(relevant(image, i, 9, 10, 10))

    def test_solve(self):
        self.assertEqual(solve(2, "input"), 17965)
        return
        self.assertEqual(solve(1, "example"), 35)
        self.assertEqual(solve(1, "input"), 5571)
        self.assertEqual(solve(2, "example"), 3351)
        self.assertEqual(solve(2, "input"), 17965)

if __name__ == "__main__":
    unittest.main()
