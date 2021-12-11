#!/usr/bin/env python3

import math
from grid import Grid


if __name__ == "__main__":
    total = 0
    grid = Grid("real", -math.inf)
    print(grid)
    for i in range(100):
        total += grid.advance_and_get_flashes()
        print(grid)
    print(total)
