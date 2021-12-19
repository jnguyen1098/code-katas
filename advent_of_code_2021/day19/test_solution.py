#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, "input"), 1)
        self.assertEqual(solve(2, "input"), 2)
        print("start")
        self.assertEqual(solve(1, "parse_test"), 1)

if __name__ == "__main__":
    unittest.main()
