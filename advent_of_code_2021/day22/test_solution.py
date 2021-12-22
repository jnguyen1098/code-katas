#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_main(self):
        self.assertEqual(solve(2, "small"), 39)
        self.assertEqual(solve(2, "new_example"), 2758514936282235)

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

    def test_get_intersection_at_a_plane(self):
        cube1 = Cube(
            xl=0, xr=4,
            yl=0, yr=4,
            zl=0, zr=4,
        )
        cube2 = Cube(
            xl=3, xr=8,
            yl=3, yr=8,
            zl=3, zr=8,
        )
        self.assertEqual(
            set(list(get_intersection(cube1, cube2))),
            set([
                (3, 3, 3),
                (4, 3, 3),
                (3, 4, 3),
                (4, 4, 3),
                (3, 3, 4),
                (4, 3, 4),
                (3, 4, 4),
                (4, 4, 4),
            ])
        ) 

    def test_get_area(self):
        cube = Cube(
            xl=0, xr=4,
            yl=0, yr=4,
            zl=0, zr=4,
        )
        self.assertEqual(get_area(cube), 125)
        cube = Cube(
            xl=1, xr=1,
            yl=1, yr=1,
            zl=1, zr=1,
        )
        self.assertEqual(get_area(cube), 1)

    def test_cube_intersect(self):
        cube1 = Cube(
            xl=0, xr=4,
            yl=0, yr=4,
            zl=0, zr=4,
        )
        cube2 = Cube(
            xl=3, xr=8,
            yl=3, yr=8,
            zl=3, zr=8,
        )
        self.assertEqual(
            get_cube_intersect(cube1, cube2),
            Cube(3, 4, 3, 4, 3, 4)
        )

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
