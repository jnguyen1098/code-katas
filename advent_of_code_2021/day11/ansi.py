#!/usr/bin/env python3

class ANSI:
    BOLD = '\x1B[1m'  # BOLD
    DIM  = '\x1B[2m'  # DIM
    UNDR = '\x1B[4m'  # UNDERLINE 
    BLNK = '\x1B[5m'  # BLINKING
    REV  = '\x1B[7m'  # INVERTED COLOURS
    HIDN = '\x1B[8m'  # HIDDEN TEXT

    RED  = "\x1B[31m"  # RED 
    GRN  = "\x1B[32m"  # GREEN
    YEL  = "\x1B[33m"  # YELLOW 
    BLU  = "\x1B[34m"  # BLUE
    MAG  = "\x1B[35m"  # MAGENTA
    CYA  = "\x1B[36m"  # CYAN
    WHT  = "\x1B[37m"  # WHITE

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
    def colourize(s, col):
        return f"{col}{s}{ANSI.RESET}"

def bold(s):
    return ANSI.colourize(s, ANSI.BOLD)

def dim(s):
    return ANSI.colourize(s, ANSI.DIM)

def undr(s):
    return ANSI.colourize(s, ANSI.UNDR)

def blnk(s):
    return ANSI.colourize(s, ANSI.BLNK)

def rev(s):
    return ANSI.colourize(s, ANSI.REV)

def hidn(s):
    return ANSI.colourize(s, ANSI.HIDN)

def red(s):
    return ANSI.colourize(s, ANSI.RED)

def grn(s):
    return ANSI.colourize(s, ANSI.GRN)

def yel(s):
    return ANSI.colourize(s, ANSI.YEL)

def blu(s):
    return ANSI.colourize(s, ANSI.BLU)

def mag(s):
    return ANSI.colourize(s, ANSI.MAG)

def cya(s):
    return ANSI.colourize(s, ANSI.CYA)

def wht(s):
    return ANSI.colourize(s, ANSI.WHT)

def lred(s):
    return ANSI.colourize(s, ANSI.LRED)

def lgrn(s):
    return ANSI.colourize(s, ANSI.LGRN)

def lyel(s):
    return ANSI.colourize(s, ANSI.LYEL)

def lblu(s):
    return ANSI.colourize(s, ANSI.LBLU)

def lmag(s):
    return ANSI.colourize(s, ANSI.LMAG)

def lcya(s):
    return ANSI.colourize(s, ANSI.LCYA)

def lwht(s):
    return ANSI.colourize(s, ANSI.LWHT)

def bred(s):
    return ANSI.colourize(s, ANSI.BRED)

def bgrn(s):
    return ANSI.colourize(s, ANSI.BGRN)

def byel(s):
    return ANSI.colourize(s, ANSI.BYEL)

def bblu(s):
    return ANSI.colourize(s, ANSI.BBLU)

def bmag(s):
    return ANSI.colourize(s, ANSI.BMAG)

def bcya(s):
    return ANSI.colourize(s, ANSI.BCYA)

def bwht(s):
    return ANSI.colourize(s, ANSI.BWHT)

def reset(s):
    return ANSI.colourize(s, ANSI.RESET)
