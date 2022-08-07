#!/usr/bin/env python3.10

word = input()

def is_vowel(char):
    return char.casefold() in "aeiou"

def get_primary_type(word: str) -> str:
    if not word[0].isupper():
        return "adjective"
    if word[0].isupper() and not is_vowel(word[0]):
        return "noun"
    return "verb"

def fancy(word: str) -> bool:
    return is_vowel(word[3])

def boring(word: str) -> bool:
    return word[4] in "xyzq"

def odd(word: str) -> bool:
    return not is_vowel(word[2])

def find_type(word: str) -> list[str]:
    primary_type = get_primary_type(word)
    types = [primary_type]
    if primary_type == "noun":
        if fancy(word):
            types.append("fancy noun")
    elif primary_type == "verb":
        if boring(word):
            types.append("boring verb")
    elif primary_type == "adjective":
        if odd(word):
            types.append("odd adjective")
    return types

for T in find_type(word):
    print(T)

