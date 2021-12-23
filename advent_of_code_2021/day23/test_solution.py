#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 12521)
        self.assertEqual(solve(1, "input"), -1)

if __name__ == "__main__":
    unittest.main()
