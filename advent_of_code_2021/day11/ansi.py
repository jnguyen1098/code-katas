#!/usr/bin/env python3
"""Colour stuff for Python."""

from typing import Any


class ANSI:
    """ANSI colour enum."""

    BOLD = "\x1B[1m"  # BOLD
    DIM = "\x1B[2m"  # DIM
    UNDR = "\x1B[4m"  # UNDERLINE
    BLNK = "\x1B[5m"  # BLINKING
    REV = "\x1B[7m"  # INVERTED COLOURS
    HIDN = "\x1B[8m"  # HIDDEN TEXT

    RED = "\x1B[31m"  # RED
    GRN = "\x1B[32m"  # GREEN
    YEL = "\x1B[33m"  # YELLOW
    BLU = "\x1B[34m"  # BLUE
    MAG = "\x1B[35m"  # MAGENTA
    CYA = "\x1B[36m"  # CYAN
    WHT = "\x1B[37m"  # WHITE

    LRED = "\x1B[91m"  # LIGHT RED
    LGRN = "\x1B[92m"  # LIGHT GREEN
    LYEL = "\x1B[93m"  # LIGHT YELLOW
    LBLU = "\x1B[94m"  # LIGHT BLUE
    LMAG = "\x1B[95m"  # LIGHT MAGENTA
    LCYA = "\x1B[96m"  # LIGHT CYAN
    LWHT = "\x1B[97m"  # LIGHT WHITE

    BRED = "\x1B[31;1m"  # BACKGROUND RED
    BGRN = "\x1B[32;1m"  # BACKGROUND GREEN
    BYEL = "\x1B[33;1m"  # BACKGROUND YELLOW
    BBLU = "\x1B[34;1m"  # BACKGROUND BLUE
    BMAG = "\x1B[35;1m"  # BACKGROUND MAGENTA
    BCYA = "\x1B[36;1m"  # BACKGROUND CYAN
    BWHT = "\x1B[37;1m"  # BACKGROUND WHITE

    RESET = "\x1B[0m"  # RESET ALL

    @staticmethod
    def concat(*args: Any) -> str:
        """Return concatenated string."""
        return "".join([str(thing) for thing in args])

    @staticmethod
    def colourize(string: str, col: str) -> str:
        """Colourize string."""
        return ANSI.concat(col, string, ANSI.RESET)


def bold(string: str) -> str:
    """Bold text."""
    return ANSI.colourize(string, ANSI.BOLD)


def dim(string: str) -> str:
    """Dim text."""
    return ANSI.colourize(string, ANSI.DIM)


def undr(string: str) -> str:
    """Underline text."""
    return ANSI.colourize(string, ANSI.UNDR)


def blnk(string: str) -> str:
    """Blink text."""
    return ANSI.colourize(string, ANSI.BLNK)


def rev(string: str) -> str:
    """Invert text colour/background."""
    return ANSI.colourize(string, ANSI.REV)


def hidn(string: str) -> str:
    """Hide text."""
    return ANSI.colourize(string, ANSI.HIDN)


def red(string: str) -> str:
    """Make text red."""
    return ANSI.colourize(string, ANSI.RED)


def grn(string: str) -> str:
    """Make text green."""
    return ANSI.colourize(string, ANSI.GRN)


def yel(string: str) -> str:
    """Make text yellow."""
    return ANSI.colourize(string, ANSI.YEL)


def blu(string: str) -> str:
    """Make text blue."""
    return ANSI.colourize(string, ANSI.BLU)


def mag(string: str) -> str:
    """Make text magenta."""
    return ANSI.colourize(string, ANSI.MAG)


def cya(string: str) -> str:
    """Make text cyan."""
    return ANSI.colourize(string, ANSI.CYA)


def wht(string: str) -> str:
    """Make text white."""
    return ANSI.colourize(string, ANSI.WHT)


def lred(string: str) -> str:
    """Make text light red."""
    return ANSI.colourize(string, ANSI.LRED)


def lgrn(string: str) -> str:
    """Make text light green."""
    return ANSI.colourize(string, ANSI.LGRN)


def lyel(string: str) -> str:
    """Make text light yellow."""
    return ANSI.colourize(string, ANSI.LYEL)


def lblu(string: str) -> str:
    """Make text light blue."""
    return ANSI.colourize(string, ANSI.LBLU)


def lmag(string: str) -> str:
    """Make text light magenta."""
    return ANSI.colourize(string, ANSI.LMAG)


def lcya(string: str) -> str:
    """Make text light cyan."""
    return ANSI.colourize(string, ANSI.LCYA)


def lwht(string: str) -> str:
    """Make text light white."""
    return ANSI.colourize(string, ANSI.LWHT)


def bred(string: str) -> str:
    """Make text 'background red'."""
    return ANSI.colourize(string, ANSI.BRED)


def bgrn(string: str) -> str:
    """Make text 'background green'."""
    return ANSI.colourize(string, ANSI.BGRN)


def byel(string: str) -> str:
    """Make text 'background yellow'."""
    return ANSI.colourize(string, ANSI.BYEL)


def bblu(string: str) -> str:
    """Make text 'background blue'."""
    return ANSI.colourize(string, ANSI.BBLU)


def bmag(string: str) -> str:
    """Make text 'background magenta'."""
    return ANSI.colourize(string, ANSI.BMAG)


def bcya(string: str) -> str:
    """Make text 'background cyan'."""
    return ANSI.colourize(string, ANSI.BCYA)


def bwht(string: str) -> str:
    """Make text 'background white'."""
    return ANSI.colourize(string, ANSI.BWHT)

