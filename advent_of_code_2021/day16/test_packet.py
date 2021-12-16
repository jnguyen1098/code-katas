#!/usr/bin/env python3

import unittest
from packet import *

class TestAllMethods(unittest.TestCase):

    def test_stream_to_hex_array(self):
        stream = "00FF"
        result = stream_to_hex_array(stream)
        self.assertEqual(result, ["00", "FF"])

if __name__ == "__main__":
    unittest.main()
