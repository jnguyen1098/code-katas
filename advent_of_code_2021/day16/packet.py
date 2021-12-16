#!/usr/bin/env python3

import re

def stream_to_hex_array(stream):
    result = re.findall(r"[0-9A-F]{2}", stream)
    assert len(stream) // 2 == len(result),\
    f"streamlen {stream} ({len(stream)}) != result len {result} ({len(result)})"
    return result
