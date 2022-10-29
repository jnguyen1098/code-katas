#!/usr/bin/env python3.10

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_displace(self):
        self.assertEqual(displace(3, 3, 2, 2, 1, 1), (0, 0))
        self.assertEqual(displace(11, 11, 3, 9, 1, 3), (4, 1))

    def test_solve(self):
        self.assertEqual(solve(1, "example1"), 7)
        self.assertEqual(solve(1, "input"), 228)
        self.assertEqual(solve(2, "example1"), 336)
        self.assertEqual(solve(2, "input"), 6818112000)

if __name__ == "__main__":
    unittest.main(failfast=True)
