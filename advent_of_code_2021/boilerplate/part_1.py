#!/usr/bin/env python3

import sys
sys.path.append("..")

from ansi import *
from comp import *

if __name__ == "__main__":
    inputname = "real"
    inputname = "example"
    inputname = "small"

    lines = []
    gen = yield_line(inputname)

    for line in gen:
        lines.append(line)

    print_arr(lines)

    print(f"{len(lines)} lines in the array")
