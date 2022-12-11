#!/usr/bin/env python3
"""Advent of Code Algorithms and Utils."""

from __future__ import annotations

import collections
import copy
import dataclasses
import doctest
import functools
import heapq
import itertools
import math
import pydantic
import random
import re
import sys
import typing
import pytest

sys.path.append("..")
sys.setrecursionlimit(100000000)

from collections import *
from dataclasses import dataclass
from functools import *
from heapq import *
from math import prod, ceil, floor, comb, fabs, factorial, floor, fmod, fsum, gcd, lcm, perm, remainder, exp, log, log10, pow, sqrt
from pprint import pprint
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Extra, Field
from typing import *

# EFFECTS: (bold|dim|undr|blnk|rev|hidn)
# COLOURS: (l|b)?(red|grn|yel|blu|mag|cya|wht)
from ansi import *

MOD = 1000000007
INF = 9999999999


class BaseModel(PydanticBaseModel):
    class Config:
        extra = Extra.forbid


class Context:
    pass

def defer(template):
    return eval(f"f'{template}'")

PRINT_LOG = True
def log(message: str, newline: bool = True) -> None:
    if PRINT_LOG:
        print(f"{message}", file=sys.stderr, end="\n" if newline else "")

def disable_logging() -> None:
    global PRINT_LOG
    PRINT_LOG = False
logging_disable = disable_logging
log_disable = disable_logging
logs_off = disable_logging
log_off = disable_logging
disable_logs = disable_logging
stop_logging = disable_logging
stop_logs = disable_logging

def enable_logging() -> None:
    global PRINT_LOG
    PRINT_LOG = True
logging_enable = enable_logging
log_enable = enable_logging
logs_on = enable_logging
log_on = enable_logging
enable_logs = enable_logging
start_logging = enable_logging
start_logs = enable_logging

def set_logging(val: bool) -> None:
    global PRINT_LOG
    PRINT_LOG = val

class DIR:
    """Directions for graphs/grid problems."""

    NW, N, NE = (-1, -1), (-1, 0), (-1, 1)
    W, E = (0, -1), (0, 1)
    SW, S, SE = (1, -1), (1, 0), (1, 1)
    DIAG = (NW, NE, SE, SW)
    HORZ = (E, W)
    VERT = (N, S)
    SURR = (*HORZ, *VERT, *DIAG)
    ADJA = (*HORZ, *VERT)


class Point:
    """2D point class."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @staticmethod
    def from_tuple(arg: tuple[int, int]) -> Point:
        if len(arg) != 2:
            raise ValueError(f"Attempted to make Point() from invalid tuple of size {len(arg)}: {arg}")
        return Point(x=arg[0], y=arg[1])

    @staticmethod
    def from_list(arg: list[int]) -> Point:
        if len(arg) != 2:
            raise ValueError(f"Attempted to make Point() from invalid list of size {len(arg)}: {arg}")
        return Point(x=arg[0], y=arg[1])

    @staticmethod
    def from_1d(displacement: int, col_size: int) -> Point:
        if col_size <= 0:
            raise ValueError(f"Attempted to make point from 1D using invalid {col_size=}")
        row, col = divmod(displacement, col_size)
        return Point(row, col)

    @staticmethod
    def coerce(*args: tuple[int, int] | list[int] | int | Point, **kwargs: int) -> Point:
        if args and kwargs:
            raise ValueError(f"Attempted to coerce point with both *args={args} and **kwargs={kwargs} - only pick one")
        if args:
            if len(args) == 1:
                if isinstance(args[0], tuple | list):
                    if isinstance(args[0][0], int) and isinstance(args[0][1], int):
                        return Point(args[0][0], args[0][1])
                    raise ValueError(f"Attempted to coerce point with tuple or list containing non-int: {args[0]}")
                elif isinstance(args[0], Point):
                    return Point(x=args[0].x, y=args[0].y)
                raise ValueError(f"Attempted to coerce point with neither tuple nor list: {args[0]}")
            elif len(args) == 2:
                if isinstance(args[0], int) and isinstance(args[1], int):
                    return Point(args[0], args[1])
                raise ValueError(f"Attempted to coerce point with non-integral arguments: {args[0]} and {args[1]}")
            raise ValueError(f"Attempted to parse *args={args} but it has invalid arguments")
        if kwargs:
            if set(kwargs.keys()) == {"x", "y"} and isinstance(kwargs["x"], int) and isinstance(kwargs["y"], int):
                return Point(kwargs["x"], kwargs["y"])
            raise ValueError(f"Attempted to parse point with invalid **kwargs={kwargs}")
        raise ValueError(f"Could not coerce/resolve point using *args={args} and **kwargs={kwargs}")

    @staticmethod
    def of(x: int, y: int) -> Point:
        return Point(x=x, y=y)

    def copy(self) -> Point:
        return Point.coerce(self)

    def to_tuple(self) -> tuple[int, int]:
        return self.x, self.y

    def to_list(self) -> list[int]:
        return [self.x, self.y]

    def to_1d(self, col_size: int) -> int:
        if self.x < 0 or self.y < 0:
            raise ValueError(f"Can't convert Point({self.x}, {self.y}) with negative value(s) to 1d")
        if col_size <= 0:
            raise ValueError(f"called to_1d() on invalid {col_size=}")
        return self.x * col_size + self.y

    def get_point(self, data: Any, x_min: int = -INF, x_max: int = INF, y_min: int = -INF, y_max: int = INF) -> Point | None:
        x, y = self.x, self.y
        disp = Point.coerce(data)
        dx, dy = disp.x, disp.y
        new_x = x + dx
        new_y = y + dy
        if x_min <= new_x <= x_max and y_min <= new_y <= y_max:
            return Point(new_x, new_y)
        return None

    def __iadd__(self, other: object) -> Point:
        if not isinstance(other, Point | tuple | list):
            raise ValueError(f"Tried adding to Point using invalid type {type(other)}: {other}")
        other_point = Point.coerce(other)  # type: ignore[arg-type]
        self.x += other_point.x
        self.y += other_point.y
        return self

    def __isub__(self, other: object) -> Point:
        if not isinstance(other, Point | tuple | list):
            raise ValueError(f"Tried subtracting from Point using invalid type {type(other)}: {other}")
        other_point = Point.coerce(other)  # type: ignore[arg-type]
        self.x -= other_point.x
        self.y -= other_point.y
        return self

    def __add__(self, other: object) -> Point:
        if not isinstance(other, Point | tuple | list):
            raise ValueError(f"Tried adding to Point using invalid type {type(other)}: {other}")
        this_copy = Point(x=self.x, y=self.y)
        this_copy += other
        return this_copy

    def __sub__(self, other: object) -> Point:
        if not isinstance(other, Point | tuple | list):
            raise ValueError(f"Tried subtracting from Point using invalid type {type(other)}: {other}")
        this_copy = Point(x=self.x, y=self.y)
        this_copy -= other
        return this_copy

    def reaches(self, other_data: Any, kernel: tuple[tuple[int, int], ...]) -> bool:
        other_point = Point.coerce(other_data)
        for dx, dy in kernel:
            if self.get_point((dx, dy)) == other_point:
                return True
        return False

    def surr(self, other_data: Any) -> bool:
        return self.reaches(other_data, DIR.SURR)

    def adja(self, other_data: Any) -> bool:
        return self.reaches(other_data, DIR.ADJA)

    def diag(self, other_data: Any) -> bool:
        return self.reaches(other_data, DIR.DIAG)

    def horz(self, other_data: Any) -> bool:
        return self.reaches(other_data, DIR.HORZ)

    def vert(self, other_data: Any) -> bool:
        return self.reaches(other_data, DIR.VERT)

    # TODO: do get_points

    def __eq__(self, other_data: object) -> bool:
        other = Point.coerce(other_data)  # type: ignore[arg-type]
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"


def test_point_init_success() -> None:
    for class_under_test in [Point(x=10, y=20), Point(10, 20)]:
        assert class_under_test.x == 10
        assert class_under_test.y == 20


def test_point_init_1d() -> None:
    assert Point.from_1d(0, 10) == Point(0, 0)
    assert Point.from_1d(9, 10) == Point(0, 9)
    assert Point.from_1d(10, 10) == Point(1, 0)
    assert Point.from_1d(11, 10) == Point(1, 1)
    assert Point.from_1d(18, 10) == Point(1, 8)
    assert Point.from_1d(19, 10) == Point(1, 9)
    assert Point.from_1d(20, 10) == Point(2, 0)
    assert Point.from_1d(239, 40) == Point(5, 39)

    for x, y in ((-10, 0), (-10, -10), (10, 0), (10, -10)):
        with pytest.raises(ValueError):
            Point.from_1d(x, y)


def test_point_to_1d() -> None:
    assert Point.from_1d(0, 10).to_1d(10) == 0
    assert Point.from_1d(9, 10).to_1d(10) == 9
    assert Point.from_1d(10, 10).to_1d(10) == 10
    assert Point.from_1d(11, 10).to_1d(10) == 11
    assert Point.from_1d(18, 10).to_1d(10) == 18
    assert Point.from_1d(19, 10).to_1d(10) == 19
    assert Point.from_1d(20, 10).to_1d(10) == 20
    assert Point.from_1d(239, 40).to_1d(40) == 239

    for col in (0, -10):
        with pytest.raises(ValueError):
            Point.from_1d(10, 5).to_1d(col)

    with pytest.raises(ValueError):
        Point(-10, -10).to_1d(10)

    with pytest.raises(ValueError):
        Point(10, -10).to_1d(10)

    with pytest.raises(ValueError):
        Point(-10, 10).to_1d(10)


@pytest.mark.parametrize(
    "runner",
    [
        lambda: Point.coerce((1, 2), x=1, y=1),
        lambda: Point.coerce((2, "d")),  # type: ignore[arg-type]
        lambda: Point.coerce(["d", 3]),  # type: ignore[list-item]
        lambda: Point.coerce("hello"),  # type: ignore[arg-type]
        lambda: Point.coerce(3, "d"),  # type: ignore[arg-type]
        lambda: Point.coerce(3, 4, 5),
        lambda: Point.coerce(x=1, y=3, z=3),
        lambda: Point.coerce(x=1),
        lambda: Point.coerce(x=1, y="3"),  # type: ignore[arg-type]
        lambda: Point.coerce(),
    ],
)
def test_coerce_point_bad(runner: Callable[[], Point]) -> None:
    with pytest.raises(ValueError):
        runner()


@pytest.mark.parametrize(
    "runner, expected",
    [
        (lambda: Point.coerce((1, 2)), Point(1, 2)),
        (lambda: Point.coerce([1, 2]), Point(1, 2)),
        (lambda: Point.coerce(3, 4), Point(3, 4)),
        (lambda: Point.coerce(x=10, y=14), Point(10, 14)),
    ],
)
def test_coerce_point_good(runner: Callable[[], Point], expected: Point) -> None:
    assert runner() == expected


def test_point_static_init_fail() -> None:
    with pytest.raises(ValueError) as exception:
        Point.from_tuple((1, 2, 3))  # type: ignore[arg-type]
    with pytest.raises(ValueError) as exception:
        Point.from_list([1, 2, 3])


def test_point_static_init() -> None:
    target = Point(10, 20)
    for clone in [Point.of(10, 20), Point.from_tuple((10, 20)), Point.from_list([10, 20])]:
        assert target == clone


def test_point_export() -> None:
    target = Point(10, 20)
    assert target.to_tuple() == (10, 20)
    assert target.to_list() == [10, 20]


def test_get_point() -> None:
    point = Point(-10, 10)
    assert point.get_point((1, 1)) == Point(-9, 11)
    assert point.get_point((-1, -1)) == Point(-11, 9)
    assert point.get_point((-1, 1)) == Point(-11, 11)
    assert point.get_point((1, -1)) == Point(-9, 9)

    other_point = Point(0, 0)
    assert not other_point.get_point((-100, 0), x_min=-50)
    assert not other_point.get_point((100, 0), x_max=50)
    assert not other_point.get_point((0, -100), y_min=-50)
    assert not other_point.get_point((0, 100), y_max=50)

    for dx, dy in DIR.SURR:
        assert not other_point.get_point((dx, dy), 0, 0, 0, 0)


def test_point_copy() -> None:
    point1 = Point(1, 2)
    point2 = point1.copy()
    assert point1 == point2 and point1 is not point2


def test_point_iadd() -> None:
    p1 = Point(1, 1)
    p1 += 1, 1
    assert p1 == Point(2, 2)
    p2 = Point(3, 4)
    p2 += [-1, -5]
    assert p2 == Point(2, -1)
    p3 = Point(3, 4)
    p3 += Point(-1, -53)
    assert p3 == Point(2, -49)
    with pytest.raises(ValueError):
        p4 = Point(1, 1)
        p4 += "d"


def test_point_isub() -> None:
    p1 = Point(1, 1)
    p1 -= 1, 1
    assert p1 == Point(0, 0)
    p2 = Point(3, 4)
    p2 -= [-1, -5]
    assert p2 == Point(4, 9)
    p3 = Point(3, 4)
    p3 -= Point(-1, -53)
    assert p3 == Point(4, 57)
    with pytest.raises(ValueError):
        p4 = Point(1, 1)
        p4 -= "d"


def test_point_add() -> None:
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    assert p1 + p2 == Point(4, 6)
    with pytest.raises(ValueError):
        print(p1 + "d")


def test_point_sub() -> None:
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    assert p1 - p2 == Point(-2, -2)
    with pytest.raises(ValueError):
        print(p1 - "d")


def test_point_adja() -> None:
    x, y = 10, 10
    point = Point(x, y)
    for dx, dy in DIR.ADJA:
        assert point.adja((x + dx, y + dy))
        assert point.adja(Point(x + dx, y + dy))
    for dx, dy in DIR.DIAG:
        assert not point.adja((x + dx, y + dy))
        assert not point.adja(Point(x + dx, y + dy))


def test_point_diag() -> None:
    x, y = 10, 10
    point = Point(x, y)
    for dx, dy in DIR.DIAG:
        assert point.diag((x + dx, y + dy))
        assert point.diag(Point(x + dx, y + dy))
    for dx, dy in DIR.ADJA:
        assert not point.diag((x + dx, y + dy))
        assert not point.diag(Point(x + dx, y + dy))


def test_point_horz() -> None:
    x, y = 10, 10
    point = Point(x, y)
    for dx, dy in DIR.HORZ:
        assert point.horz((x + dx, y + dy))
        assert point.horz(Point(x + dx, y + dy))
    for dx, dy in DIR.VERT:
        assert not point.horz((x + dx, y + dy))
        assert not point.horz(Point(x + dx, y + dy))


def test_point_vert() -> None:
    x, y = 10, 10
    point = Point(x, y)
    for dx, dy in DIR.VERT:
        assert point.vert((x + dx, y + dy))
        assert point.vert(Point(x + dx, y + dy))
    for dx, dy in DIR.HORZ:
        assert not point.vert((x + dx, y + dy))
        assert not point.vert(Point(x + dx, y + dy))


def test_point_surr() -> None:
    x, y = 10, 10
    point = Point(x, y)
    for dx, dy in DIR.SURR:
        assert point.surr((x + dx, y + dy))
        assert point.surr(Point(x + dx, y + dy))
    for dx, dy in DIR.SURR:
        assert not point.surr((x + dx + 10, y + dy + 10))
        assert not point.surr(Point(x + dx + 10, y + dy + 10))


def test_point_eq() -> None:
    assert Point(10, 10) == (10, 10)
    assert Point(11, 11) != (11, 12)
    assert Point(11, 11) != (12, 11)
    assert Point(99, 99) != (0, 0)

    assert Point(10, 10) == Point(10, 10)
    assert Point(11, 11) != Point(11, 12)
    assert Point(11, 11) != Point(12, 11)
    assert Point(99, 99) != Point(0, 0)

    assert Point(10, 10) == [10, 10]
    assert Point(11, 11) != [11, 12]
    assert Point(11, 11) != [12, 11]
    assert Point(99, 99) != [0, 0]


def test_point_repr_str() -> None:
    assert str(Point(1, 2)) == "Point(x=1, y=2)"
    assert repr(Point(1, 2)) == "Point(x=1, y=2)"


def expect(actual: Any, expected: Any) -> tuple[bool, str]:
    """Compares two values and spits out equality and message."""
    if type(actual) != type(expected):
        return False, f"FAIL: {actual=} has type {type(actual)} vs {expected=} which has type {type(expected)}"
    if actual != expected:
        ret_msg = f"FAIL: Expected {expected} but got {actual}"
        ret_sta = False
        return ret_sta, ret_msg
    return True, "PASS"


def test_expect() -> None:
    assert expect(1, "1") == (False, "FAIL: actual=1 has type <class 'int'> vs expected='1' which has type <class 'str'>")
    assert expect(1, 2) == (False, "FAIL: Expected 2 but got 1")
    assert expect("1", "1") == (True, "PASS")


def get_point(old: tuple[int, int], new: tuple[int, int], rows: int, cols: int) -> tuple[int, int] | None:
    """Translates a point given a displacement tuple."""
    new_x = old[0] + new[0]
    new_y = old[1] + new[1]
    if 0 <= new_x < rows and 0 <= new_y < cols:
        return new_x, new_y
    return None


def test_get_point_old() -> None:
    assert not get_point((1, 1), (1, 1), 0, 0)
    assert get_point((5, 5), (5, 5), 11, 11) == (10, 10)


def print_arr(arr: Iterable[Iterable[Any]], sep: str = "") -> None:
    """Array printing but prettier."""
    print("\n".join([sep.join([str(cell) for cell in row]) for row in arr]))


def test_print_arr() -> None:
    print_arr([[]])


revdict = lambda dt: {v: k for k, v in dt.items()}
reverse_dictionary = revdict
get_reversed_dictionary = revdict
inverse_dictionary = revdict
invert_dictionary = revdict
swap_dictionary = revdict
strsep = lambda text, sep=None: list(text.strip().split(sep))
intsep = lambda text, sep=None: list(map(int, text.strip().split(sep)))
intgrid = lambda text: list(map(int, [char for char in text.strip()]))


def parse(pattern: str, text: str) -> tuple[str | Any, ...]:
    if (result := re.fullmatch(pattern, text)) is None:
        raise RuntimeError(f"re.fullmatch() on {pattern=} failed to parse line of length {len(text)}: '{text}'")
    return result.groups()


def test_parse() -> None:
    with pytest.raises(RuntimeError):
        parse("hello", "hellod")
    assert parse("hello", "hello") == ()
    assert parse("(hello)", "hello") == ("hello",)
    assert parse(r"(\w+) (\d+)", "hello 100") == ("hello", "100")


def yield_line(filename: str) -> Iterable[str]:
    with open(filename, "r") as file_p:
        for line in file_p.read().splitlines():
            yield line


def test_yield_line() -> None:
    for line in yield_line(__name__ + ".py"):
        pass

# CRT stolen from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python
def get_modular_multiplicative_inverse(a: int, m: int) -> int:
    """
    Calculates the modular multiplicative inverse of a and m such that:
    \b
    ax === 1 (mod m)
    \b
    :param a: the operand we are applying the operation to
    :param m: the modulus relevant to the answer
    :return: the inverse of a % m
    """
    b0 = m
    x0, x1 = 0, 1
    if m == 1: return 1
    while a > 1:
        q = a // m
        a, m = m, a%m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

mul_inv = get_modular_multiplicative_inverse
modular_multiplicative_inverse = get_modular_multiplicative_inverse
multiplicative_modular_inverse = get_modular_multiplicative_inverse
solve_multiplicative_inverse = get_modular_multiplicative_inverse
mod_inverse = get_modular_multiplicative_inverse
solve_mod_inverse = get_modular_multiplicative_inverse
get_mod_inverse = get_modular_multiplicative_inverse
get_mul_inv = get_modular_multiplicative_inverse

@lru_cache(None)
def solve_chinese_remainder_theorem(nums: tuple[int, ...], mods: tuple[int, ...]) -> int:
    """
    Solves the Chinese Remainder Theorem
    \b
    x === a1 (mod m1)
    \b
    x === a2 (mod m2)
    \b
    x === a3 (mod m3)
    \b
    :param nums: the desired residues [a1, a2, a3, ...]
    :param mods: the moduli of the desired residues [m1, m2, m3, ...]
    :return: result of the CRT
    """
    final_sum = 0
    prod = reduce(lambda acc, b: acc*b, mods)
    for n_i, a_i in zip(mods, nums, strict=True):
        p = prod // n_i
        final_sum += a_i * mul_inv(p, n_i) * p
    return final_sum % prod

crt = solve_chinese_remainder_theorem
chinese_remainder = solve_chinese_remainder_theorem
chinese_remainder_theorem = solve_chinese_remainder_theorem
solve_crt = solve_chinese_remainder_theorem
get_chinese_remainder_theorem_solution = solve_chinese_remainder_theorem
get_crt = solve_chinese_remainder_theorem
