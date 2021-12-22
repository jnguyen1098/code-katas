#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_get_cubes(self):
        return
        get_cubes(10, 12, 10, 12, 10, 12)
        """
        expected = set([
            [10,10,10],
            [10,10,11],
            [10,10,12],
            [10,11,10],
            [10,11,11],
            [10,11,12],
            [10,12,10],
            [10,12,11],
            [10,12,12],
            [11,10,10],
            [11,10,11],
            [11,10,12],
            [11,11,10],
            [11,11,11],
            [11,11,12],
            [11,12,10],
            [11,12,11],
            [11,12,12],
            [12,10,10],
            [12,10,11],
            [12,10,12],
            [12,11,10],
            [12,11,11],
            [12,11,12],
            [12,12,10],
            [12,12,11],
            [12,12,12],
        ])
        """


    def test_solve(self):
        print("small")
        self.assertEqual(solve(1, "small"), 39)
        print("example")
        self.assertEqual(solve(1, "example"), 590784)
        print("actual input")
        self.assertEqual(solve(1, "input"), 647076)

if __name__ == "__main__":
    unittest.main(failfast=True)
