#!/usr/bin/env python3

import unittest
from packet import *

class TestAllMethods(unittest.TestCase):

    def test_stream_to_hex_array_simple(self):
        stream = "00FF"
        result = stream_to_hex_array(stream)
        self.assertEqual(result, ["00", "FF"])

    def test_stream_to_hex_array_complex(self):
        stream_arr = []
        for i in range(0x00, 0xFF + 1):
            stream_arr.append(hex(i)[2:].upper().zfill(2))
        stream = "".join(stream_arr)
        result = stream_to_hex_array(stream)
        self.assertEqual(result, stream_arr)

if __name__ == "__main__":
    unittest.main()
