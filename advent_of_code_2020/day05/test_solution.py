#!/usr/bin/env python3.10

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, "example1"), 357)
        self.assertEqual(solve(1, "example2"), 567)
        self.assertEqual(solve(1, "example3"), 119)
        self.assertEqual(solve(1, "example4"), 820)
        self.assertEqual(solve(1, "example4"), -1)

if __name__ == "__main__":
    unittest.main(failfast=True)
