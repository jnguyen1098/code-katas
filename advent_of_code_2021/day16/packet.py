#!/usr/bin/env python3
"""Packet module."""

import re
from typing import List


class PacketRuntimeException(Exception):
    """Just a fancy exception name."""


def die(message: str) -> None:
    """Raise message and then die."""
    raise PacketRuntimeException(message)


def stream_to_hex_array(stream: str) -> List[str]:
    """Convert stream string to array of padded hex."""
    result = re.findall(r"[0-9A-F]{2}", stream)
    assert len(stream) // 2 == len(
        result
    ), f"streamlen {stream} ({len(stream)}) != result len {result} ({len(result)})"
    return result


def number_to_binary(num: int, pad: int = 0) -> str:
    """Convert integer to padded binary string."""
    return format(num, "b").zfill(pad)


def read(string: str, left: int, right: int) -> str:
    """Read string on inclusive indices [left, right], returning read bytes."""
    if left <= right:
        die(f"invalid read(), l ({left}) > r ({right})")
    return string[left : right + 1]
