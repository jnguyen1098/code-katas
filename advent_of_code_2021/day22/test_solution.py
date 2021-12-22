#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_get_intersection_at_a_single_point(self):
        cube1 = Cube(
            xl=0, xr=4,
            yl=0, yr=4,
            zl=0, zr=4,
        )
        cube2 = Cube(
            xl=4, xr=8,
            yl=4, yr=8,
            zl=4, zr=8,
        )
        self.assertEqual(list(get_intersection(cube1, cube2)), [(4, 4, 4)]) 

    def test_solve_1(self):
        self.assertEqual(solve(1, "small"), 39)
        self.assertEqual(solve(1, "example"), 590784)
        self.assertEqual(solve(1, "input"), 647076)

    def test_solve_2(self):
        self.assertEqual(solve(1, "new_example"), 474140)
        self.assertEqual(solve(2, "new_example"), 2758514936282235)
        self.assertEqual(solve(2, "input"), -1)

if __name__ == "__main__":
    unittest.main(failfast=True)
