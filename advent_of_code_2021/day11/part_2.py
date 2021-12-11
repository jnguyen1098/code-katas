#!/usr/bin/env python3

import math

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

exit()

class Grid:
    def __init__(self, filename, sentinel):
        lines = open(filename, "r").read().splitlines()
        self.grid = [[int(char) for char in line] for line in lines]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.sentinel = sentinel

    def __str__(self):
        result = []
        for row in self.grid:
            row_line = []
            for char in row:
                row_line.append(bold(char) if char == 0 else dim(char))
            result.append("".join(row_line))
        result.append("")
        return "\n".join(result)

    def add_to_all_cells(self, amount):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] += amount

    def add_around_cell(self, x, y, amount):
        MOVES = ((-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1),  (1, 0),  (1, 1),)
        for move in MOVES:
            new_x = x + move[0]
            new_y = y + move[1]
            if new_x >= 0 and new_x < self.rows and new_y >= 0 and new_y < self.cols:
                self.grid[new_x][new_y] += amount

    def get_flash(self):
        fls = set()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] > 9:
                    fls.add((i, j))
        return fls

    def get_new_flash(self, old_flash):
        return self.get_flash() - old_flash

    def flash(self, fls):
        for x, y in fls:
            self.add_around_cell(x, y, 1)
            self.grid[x][y] = self.sentinel

    def clean_board(self):
        cnt = 0
        for i in range(self.rows):
           for j in range(self.cols):
                if self.grid[i][j] == self.sentinel:
                    self.grid[i][j] = 0
                    cnt += 1
        return cnt

    def advance_and_get_flashes(self):
        self.add_to_all_cells(1)
        while fls := self.get_flash():
            self.flash(fls)
        return self.clean_board()


if __name__ == "__main__":
    total = 0
    grid = Grid("example", -math.inf)
    print(grid)
    for i in range(3):
        if grid.advance_and_get_flashes() == grid.rows * grid.cols:
            print(i + 1)
            exit()
        print(grid)