#!/usr/bin/env python3.10

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 514579)
        self.assertEqual(solve(1, "input"), 145875)
        self.assertEqual(solve(2, "example2"), 241861950)
        self.assertEqual(solve(2, "input2"), 69596112)

if __name__ == "__main__":
    unittest.main(failfast=True)
