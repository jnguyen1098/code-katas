#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 58)
        self.assertEqual(solve(1, "example"), -1)

if __name__ == "__main__":
    unittest.main()
