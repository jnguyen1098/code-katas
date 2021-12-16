#!/usr/bin/env python3
"""Unit tests."""

import unittest

import packet


class TestAllMethods(unittest.TestCase):
    """Test all methods class."""

    def test_die(self) -> None:
        """Test the die function."""
        with self.assertRaises(packet.PacketRuntimeException):
            packet.die("this should raise something")

    def test_stream_to_hex_array_simple(self) -> None:
        """Testing the hex array conversion function."""
        stream = "00FF"
        result = packet.stream_to_hex_array(stream)
        self.assertEqual(result, ["00", "FF"])

    def test_stream_to_hex_array_complex(self) -> None:
        """Testing the hex array conversion function."""
        stream_arr = []
        for i in range(0x00, 0xFF + 1):
            stream_arr.append(hex(i)[2:].upper().zfill(2))
        stream = "".join(stream_arr)
        result = packet.stream_to_hex_array(stream)
        self.assertEqual(result, stream_arr)

    def test_number_to_binary(self) -> None:
        """Test number to binary."""
        self.assertEqual(packet.number_to_binary(12, 8), "00001100")
        self.assertEqual(packet.number_to_binary(12), "1100")
        self.assertEqual(packet.number_to_binary(12, 0), "1100")
        self.assertEqual(packet.number_to_binary(255, 0), "11111111")
        self.assertEqual(packet.number_to_binary(0, 0), "0")
        self.assertEqual(packet.number_to_binary(0, 8), "00000000")


if __name__ == "__main__":
    unittest.main()
