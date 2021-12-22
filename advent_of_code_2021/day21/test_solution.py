#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 739785)
        self.assertEqual(solve(1, "input"), 752247)
        self.assertEqual(solve(2, "example"), 444356092776315)
        self.assertEqual(solve(2, "input"), 221109915584112)

if __name__ == "__main__":
    unittest.main(failfast=True)
