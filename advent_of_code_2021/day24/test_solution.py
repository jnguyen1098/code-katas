#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_simulate_chunk_1(self):
        instructions = parse_instructions("chunk1")
        print("chunk1")
        for i in range(1, 10):
            self.assertEqual(chunk1(i), simulate(instructions, str(i)))
            print(chunk1(i))
        print()

    def test_simulate_chunk_2(self):
        instructions = parse_instructions("chunk2")
        print("chunk1")
        for i in range(1, 10):
            for j in range(22, 111):
                self.assertEqual(chunk2(i, j), simulate(instructions, str(i), x=i, z=j))
                print(chunk2(i, j))
        print()

    def test_solve(self):
        return
        self.assertEqual(solve(1, "input"), 1)
        self.assertEqual(solve(2, "input"), 2)

if __name__ == "__main__":
    unittest.main()
