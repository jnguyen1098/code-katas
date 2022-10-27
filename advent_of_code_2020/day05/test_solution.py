#!/usr/bin/env python3.10

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_get_row(self):
        self.assertEqual(get_row("FFFFFFF..."), 0)
        self.assertEqual(get_row("BBBBBBB..."), 127)
        self.assertEqual(get_row("FBFBBFFRLR"), 44)

    def test_get_seat(self):
        self.assertEqual(get_seat(".......LLL"), 0)
        self.assertEqual(get_seat(".......RRR"), 7)
        self.assertEqual(get_seat(".......RLR"), 5)
        self.assertEqual(get_seat(".......RLL"), 4)

    def test_get_id(self):
        self.assertEqual(get_id("FBFBBFFRLR"), 357)
        self.assertEqual(get_id("BFFFBBFRRR"), 567)
        self.assertEqual(get_id("FFFBBBFRRR"), 119)
        self.assertEqual(get_id("BBFFBBFRLL"), 820)

    def test_solve(self):
        self.assertEqual(solve(1, "example1"), 357)
        self.assertEqual(solve(1, "example2"), 567)
        self.assertEqual(solve(1, "example3"), 119)
        self.assertEqual(solve(1, "example4"), 820)
        self.assertEqual(solve(1, "input"), 959)

if __name__ == "__main__":
    unittest.main(failfast=True)
