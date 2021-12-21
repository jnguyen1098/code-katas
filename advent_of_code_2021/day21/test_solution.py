#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_serialize(self):
        self.assertEqual(encode(1, 2, 3, 4, 1), "1,2|3,4|1")
        self.assertEqual(encode(1, 2, 3, 4, 2), "1,2|3,4|2")
        self.assertEqual(encode(9999, 888, 77, 6, 1), "9999,888|77,6|1")
        self.assertEqual(encode(9999, 888, 77, 6, 2), "9999,888|77,6|2")
        self.assertEqual(encode(9999, 1, 77, 10, 1), "9999,1|77,10|1")
        self.assertEqual(encode(9999, 1, 77, 10, 2), "9999,1|77,10|2")

    def test_deserialize(self):
        self.assertEqual(decode("1,2|3,4|1"), (1, 2, 3, 4, 1))
        self.assertEqual(decode("9999,888|77,6|1"), (9999, 888, 77, 6, 1))

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 739785)
        self.assertEqual(solve(1, "input"), 752247)
        self.assertEqual(solve(2, "example"), 444356092776315)
        self.assertEqual(solve(2, "input"), 221109915584112)

if __name__ == "__main__":
    unittest.main(failfast=True)
