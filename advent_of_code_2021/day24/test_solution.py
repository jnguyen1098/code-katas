#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_simulate_chunk_1(self):
        instructions = parse_instructions("chunk1")
        print("chunk1")
        for i in range(1, 10):
            self.assertEqual(chunk1(i), simulate(instructions, str(i)))
            print(f"abstraction={chunk1(i)} simulation={simulate(instructions, str(i))}")
        print()

    def test_simulate_chunk_2(self):
        instructions = parse_instructions("chunk2")
        print("chunk2")
        for i in range(1, 10):
            for j in range(22, 111, 11):
                self.assertEqual(chunk2(w=i, z=j), simulate(instructions, str(i), z=j))
                print(chunk2(i, j))
        print()

    def test_simulate_chunk_3(self):
        instructions = parse_instructions("chunk3")
        print("chunk3")
        for w in range(1, 10):
            for z in range(22, 111, 11):
                print("w", w, "z", z)
                w_arg = w
                z_arg = (z + 26) + (w + 10)
                chunk_result = chunk3(w=w_arg, z=z_arg)
                self.assertEqual(chunk_result, simulate(instructions, str(w_arg), z=z_arg))
                print(chunk_result)
        print()

    def test_simulate_chunk_4(self):
        instructions = parse_instructions("chunk4")
        print("chunk4")
        for w in range(1, 10):
            for z in range(22, 111, 11):
                print("w", w, "z", z)
                w_arg = w
                z_arg = (z // 26 * 26) + (w + 5)
                chunk_result = chunk4(w=w_arg, z=z_arg)
                self.assertEqual(chunk_result, simulate(instructions, str(w_arg), z=z_arg))
                print(chunk_result)
        print()

    def test_solve(self):
        return
        self.assertEqual(solve(1, "input"), 1)
        self.assertEqual(solve(2, "input"), 2)

if __name__ == "__main__":
    unittest.main()
