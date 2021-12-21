#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_roll(self):
        thing = []
        pointer = Pointer(1)
        for i in range(10):
            thing.append(roll(pointer))
        self.assertEqual(thing, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 739785)
        self.assertEqual(solve(1, "input"), 1)
        self.assertEqual(solve(2, "example"), 2)
        self.assertEqual(solve(2, "input"), 2)

if __name__ == "__main__":
    unittest.main()
