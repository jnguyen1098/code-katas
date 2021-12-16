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

    def test_number_to_binary(self):
        self.assertEqual(number_to_binary(12, 8), "00001100")
        self.assertEqual(number_to_binary(12), "1100")
        self.assertEqual(number_to_binary(12, 0), "1100")
        self.assertEqual(number_to_binary(255, 0), "11111111")
        self.assertEqual(number_to_binary(0, 0), "0")
        self.assertEqual(number_to_binary(0, 8), "00000000")

if __name__ == "__main__":
    unittest.main()
