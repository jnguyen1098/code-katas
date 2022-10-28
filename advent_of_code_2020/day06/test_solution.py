#!/usr/bin/env python3.10

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 11)
        self.assertEqual(solve(1, "input"), 6680)
        self.assertEqual(solve(2, "example"), 6)
        self.assertEqual(solve(2, "input"), 3117)

if __name__ == "__main__":
    unittest.main(failfast=True)
