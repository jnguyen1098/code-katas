#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_get_intersection(self):
        get_intersection(None, None)

    def test_solve_1(self):
        self.assertEqual(solve(1, "small"), 39)
        self.assertEqual(solve(1, "example"), 590784)
        self.assertEqual(solve(1, "input"), 647076)

    def test_solve_2(self):
        self.assertEqual(solve(1, "new_example"), 474140)
        self.assertEqual(solve(2, "new_example"), 2758514936282235)
        self.assertEqual(solve(2, "input"), -1)

if __name__ == "__main__":
    unittest.main(failfast=True)
