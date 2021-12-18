#!/usr/bin/env python3

import unittest
from solution import *

class TestAll(unittest.TestCase):

    def test_str_to_pair(self):
        self.assertEqual(str_to_pair("[1,2]"), [1, 2])
        self.assertEqual(str_to_pair("[1,[2,3]]"), [1, [2,3]])

if __name__ == "__main__":
    unittest.main()
