#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

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

    def test_solve(self):
        self.assertEqual(solve(1, "example"), 58)
        self.assertEqual(solve(1, "example"), -1)

if __name__ == "__main__":
    unittest.main()
