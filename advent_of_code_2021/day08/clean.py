#!/usr/bin/env python3

import math

inputname = "small"

lines = open(inputname, "r").read().splitlines()

for idx, line in enumerate(lines):
    print(idx, line)
print("linecount:", len(lines))
