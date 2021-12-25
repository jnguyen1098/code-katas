#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_simulate(self):
        instructions = parse_instructions("chunk1")
        for i in range(1, 10):
            print(simulate(instructions, str(i)))

    def test_solve(self):
        return
        self.assertEqual(solve(1, "input"), 1)
        self.assertEqual(solve(2, "input"), 2)

if __name__ == "__main__":
    unittest.main()
