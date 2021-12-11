#!/usr/bin/env python3

import math
from grid import Grid


if __name__ == "__main__":
    grid = Grid("real", -math.inf)
    print(grid)
    for i in range(1000000):
        if grid.advance_and_get_flashes() == grid.rows * grid.cols:
            print(i + 1)
            exit()
        print(grid)
