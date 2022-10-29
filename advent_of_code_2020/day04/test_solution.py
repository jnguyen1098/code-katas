#!/usr/bin/env python3.10

import unittest
from solution import *

def generate_example_lines():
    lines = [
        "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
        "byr:1937 iyr:2017 cid:147 hgt:183cm",
        "",
        "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
        "hcl:#cfa07d byr:1929",
        "",
        "hcl:#ae17e1 iyr:2013",
        "eyr:2024",
        "ecl:brn pid:760753108 byr:1931",
        "hgt:179cm",
        "",
        "hcl:#cfa07d eyr:2025 pid:166559648",
        "iyr:2011 ecl:brn hgt:59in",
    ]
    return lines

class TestAll(unittest.TestCase):

    def test_split_lines_into_key_value_pairs(self):
        lines = generate_example_lines()
        self.assertEqual(
            split_lines_into_key_value_pairs([lines[0], "", lines[1]]),
            [
                ("ecl", "gry"), ("pid", "860033327"), ("eyr", "2020"), ("hcl", "#fffffd"),
                ("byr", "1937"), ("iyr", "2017"), ("cid", "147"), ("hgt", "183cm"),
            ]
        )

    def test_create_passport(self):
        lines = generate_example_lines()
        kv_pairs = split_lines_into_key_value_pairs([lines[0]])
        passport = create_passport(kv_pairs)
        expected_passport = {
            "ecl": "gry",
            "pid": "860033327",
            "eyr": "2020",
            "hcl": "#fffffd",
        }
        self.assertEqual(passport, expected_passport)

    def test_solve(self):
        self.assertEqual(solve(1, "example1"), 2)
        self.assertEqual(solve(1, "input"), 239)
        self.assertEqual(solve(2, "example2"), 4)
        self.assertEqual(solve(2, "input"), 188)

if __name__ == "__main__":
    unittest.main(failfast=True)
