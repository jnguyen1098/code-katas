#!/usr/bin/env python3.10

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, "example1"), 5)
        self.assertEqual(solve(1, "input"), 1337)
        self.assertEqual(solve(2, "example1"), 8)
        self.assertEqual(solve(2, "input"), 1358)

if __name__ == "__main__":
    unittest.main(failfast=True)
