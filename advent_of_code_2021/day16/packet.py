#!/usr/bin/env python3

import re

def stream_to_hex_array(stream):
    result = re.findall(r"[0-9A-F]{2}", stream)
    assert len(stream) // 2 == len(result),\
    f"streamlen {stream} ({len(stream)}) != result len {result} ({len(result)})"
    return result

def number_to_binary(num, pad=0):
    return format(num, "b").zfill(pad)

def read(string, l, r):
    assert l <= r, f"invalid read(), l ({l}) > r ({r})"
    return r - l + 1
