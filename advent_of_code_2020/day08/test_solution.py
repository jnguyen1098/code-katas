#!/usr/bin/env python3.10

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 5)
        self.assertEqual(solve(1, "input"), 1)
        self.assertEqual(solve(2, "example"), 2)
        self.assertEqual(solve(2, "input"), 2)

if __name__ == "__main__":
    unittest.main(failfast=True)
