#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_init(self):
        cols = [[], [[]], [[[]]]]
        cols = [["A", "B", "C", "D"], ["A", "B", "C"], ["A", "B"], ["A"]]
        game = Game(cols)
        self.assertEqual(game.cols, cols)
        print(game)

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 12521)
        self.assertEqual(solve(1, "input"), 10411)

if __name__ == "__main__":
    unittest.main()
