#!/usr/bin/env python3.10

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 4)
        self.assertEqual(solve(1, "input"), 302)
        self.assertEqual(solve(2, "example"), 32)
        self.assertEqual(solve(2, "example2"), 126)
        self.assertEqual(solve(2, "input"), 4165)

if __name__ == "__main__":
    unittest.main(failfast=True)
