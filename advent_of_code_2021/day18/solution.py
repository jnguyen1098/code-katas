#!/usr/bin/env python3

import json
import sys
sys.path.append("..")

from ansi import *
from comp import *

def get_pair(string):
    arr = json.loads(string)
    return [arr[0], arr[1]]

def get_pair_from_idx(tokens, l, r):
    tmp = []
    for i in range(l, r + 1):
        tmp.append(str(tokens[i]))
    return get_pair("".join(tmp))

def peek(string, i):
    return string[i + 1] if i + 1 < len(string) else None

def tokenize(string):
    tokens = []
    num = 0
    for idx, char in enumerate(string):
        if char.isspace():
            continue
        elif char in ["[", "]", ","]:
            tokens.append(char)
        else:
            num *= 10
            num += int(char)
            if peek(string, idx) is None or not peek(string, idx).isdigit():
                tokens.append(num)
                num = 0
    return tokens

def get_explode_idxs(tokens):
    bal = 0
    l, r = None, None

    for idx, item in enumerate(tokens):
        if item == "[":   bal += 1
        elif item == "]": bal -= 1
        if bal == 5:
            if l is None:
                l = idx
            else:
                r = idx
        elif l and r:
            return l, r + 1

def remove_token(tokens, idx):
    return [token for token in tokens if token != tokens[idx]]

def remove_range(tokens, l, r):
    result = []
    for i in range(len(tokens)):
        if not (l <= i <= r):
            result.append(tokens[i])
    return result

def replace_range(tokens, l, r, replacement):
    tmp = remove_range(tokens, l, r)
    tmp.insert(l, replacement)
    return tmp

def get_first_left_num(tokens, i):
    i -= 1
    while i >= 0:
        if isinstance(tokens[i], int):
            return i
        i -= 1
    return None

def get_first_right_num(tokens, i):
    i += 1
    while i < len(tokens):
        if isinstance(tokens[i], int):
            return i
        i += 1
    return None

def needs_to_explode(tokens):
    return get_explode_idxs(tokens) is not None

def explode(tokens):
    if not needs_to_explode(tokens):
        return tokens
    explode_l, explode_r = get_explode_idxs(tokens)
    pair = get_pair_from_idx(tokens, explode_l, explode_r)
    if l_idx := get_first_left_num(tokens, explode_l):
        tokens[l_idx] += pair[0]
    if r_idx := get_first_right_num(tokens, explode_r):
        tokens[r_idx] += pair[1]
    return replace_range(tokens, explode_l, explode_r, 0)

def needs_to_split(tokens):
    for token in tokens:
        if isinstance(token, int) and token > 9:
            return True
    return False

def get_split_idx(tokens):
    if not needs_to_split(tokens):
        return None
    for idx, token in enumerate(tokens):
        if isinstance(token, int) and token > 9:
            return idx
    assert False, "This should never be reached"

def split_int(num):
    if num % 2 == 0: return num // 2, num // 2
    return num // 2, num // 2 + 1

def split(tokens):
    if not needs_to_split(tokens):
        return tokens
    spl_i = get_split_idx(tokens)
    spl_l, spl_r = split_int(tokens[spl_i])
    return tokens[0 : spl_i] + ["[", spl_l, ",", spl_r, "]"] + tokens[spl_i + 1:]

def concat_tokens(tokens1, tokens2):
    return ["["] + tokens1 + [","] + tokens2 + ["]"]

def add_lines(tokens1, tokens2):
    cat = concat_tokens(tokens1, tokens2)
    while needs_to_explode(cat) or needs_to_split(cat):
        if needs_to_explode(cat):
            cat = explode(cat)
        elif needs_to_split(cat):
            cat = split(cat)
    return cat

def pipeline(list_of_token_lists):
    result = list_of_token_lists[0]
    for i in range(1, len(list_of_token_lists)):
        result = add_lines(result, list_of_token_lists[i])
    return result

def get_magnitude(tokens):
    pair = get_pair("".join([str(tok) for tok in tokens]))
    l, r = pair[0], pair[1]

    magnitude = 0
    
    if isinstance(l, int):
        magnitude += 3 * l
    else:
        magnitude += 3 * get_magnitude(tokenize(json.dumps(l)))

    if isinstance(r, int):
        magnitude += 2 * r
    else:
        magnitude += 2 * get_magnitude(tokenize(json.dumps(r)))

    return magnitude

def solve(prob, inputname):
    lines = [tokenize(line) for line in yield_line(inputname)]

    if prob == 1:
        return get_magnitude(pipeline(lines))
    elif prob == 2:
        return 2
    else:
        print("Invalid problem code")
        exit()

if __name__ == "__main__":
    print(red(rev(f"Part 1")) + f": {solve(1, 'input')}\n")
    print(red(rev(f"Part 2")) + f": {solve(2, 'input')}\n")
