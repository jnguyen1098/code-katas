#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_dim(self):
        board = create_board("example")
        self.assertEqual(len(board.data), 9)
        for i in range(9):
            self.assertEqual(len(board.data[i]), 10)

    def test_incr(self):
        board = create_board("example")
        self.assertEqual(board.right(0), 1)
        self.assertEqual(board.right(9), 0)
        self.assertEqual(board.down(0), 1)
        self.assertEqual(board.down(8), 0)

    def test_advance(self):
        board = create_board("example")
        self.assertEqual(str(board),
"""v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""")
        board.advance()
        self.assertEqual(str(board),
"""....>.>v.>
v.v>.>v.v.
>v>>..>v..
>>v>v>.>.v
.>v.v...v.
v>>.>vvv..
..v...>>..
vv...>>vv.
>.v.v..v.v""")
        for _ in range(56):
            board.advance()
        self.assertEqual(board.advance(), 0)
        self.assertEqual(str(board),
"""..>>v>vv..
..v.>>vv..
..>>v>>vv.
..>>>>>vv.
v......>vv
v>v....>>v
vvv.....>>
>vv......>
.>v.vv.v..""")

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 58)
        self.assertEqual(solve(1, "input"), 384)

if __name__ == "__main__":
    unittest.main()
