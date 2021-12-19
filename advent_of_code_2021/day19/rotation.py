#!/usr/bin/env python3

# given (x, y, z)

rotations = [
# x
    # negative
        # north up
        [-x, y, -z],
        # east up
        [-x, y, z],
        # south up
        [-x, -y, z],
        # west up
        [-x, -y, -z],
    # positive
        # north up
        [x, y, z],
        # east up
        [x, y, -z],
        # south up
        [x, -y, -z],
        # west up
        [x, -y, z],
# y
    # negative
        # north up
        [x, -y, -z],
        # east up
        [-x, -y, -z],
        # south up
        [-x, -y, z],
        # west up
        [x, -y, z],
    # positive
        # north up
        [x, y, z],
        # east up
        [-x, y, z],
        # south up
        [-x, y, -z],
        # west up
        [x, y, -z],
# z
    # negative
        # north up
        [x, y, -z],
        # east up
        [-x, y, -z],
        # south up
        [-x, -y, -z],
        # west up
        [x, -y, -z],
    # positive
        # north up
        [-x, y, z],
        # east up
        [x, y, z],
        # south up
        [x, -y, z],
        # west up
        [-x, -y, z],
]

print("hello")
