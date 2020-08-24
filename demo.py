#!/usr/bin/env python3

from mines import Grid
from sys import argv
import argparse
import curses


BLACK = 0x0
RED = 0x1
GREEN = 0x2
YELLOW = 0x3
BLUE = 0x4
MAGENTA = 0x5
CYAN = 0x6
WHITE = 0x7
BRIGHT_BLACK = 0x8
BRIGHT_RED = 0x9
BRIGHT_GREEN = 0xA
BRIGHT_YELLOW = 0xB
BRIGHT_BLUE = 0xC
BRIGHT_MAGENTA = 0xD
BRIGHT_CYAN = 0xE
BRIGHT_WHITE = 0xF

cellColors = {
    "1": BRIGHT_BLUE,
    "2": GREEN,
    "3": BRIGHT_RED,
    "4": BLUE,
    "5": RED,
    "6": CYAN,
    "7": BRIGHT_WHITE,
    "8": BRIGHT_BLACK,
    "@": BRIGHT_YELLOW,
    "*": YELLOW,
    "#": YELLOW,
    "X": BRIGHT_MAGENTA,
    "-": BRIGHT_BLACK,
}


def printGrid(stdscr, args, grid):
    lose = False  # TODO need win/lose function
    stdscr.move(0, 0)
    for r in range(args.rows):
        for c in range(args.cols):
            x, y = c * 2 + 1, r
            cell = grid[(r, c)]

            if not lose and cell == "X":
                cell = "#"
            if not lose and cell == "*":
                cell = "-"
            if cell != "0":
                stdscr.addstr(y, x, cell, curses.color_pair(cellColors[cell]))
            else:
                stdscr.addstr(y, x, " ")

    stdscr.refresh()


def main(stdscr, args):
    # curses init
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i if args.color else -1, -1)

    # game init
    x, y = 0, 0
    grid = Grid(args.rows, args.cols, args.mines)

    # game loop
    while True:
        printGrid(stdscr, args, grid)

        stdscr.move(y, 2 * x + 1)
        curses.curs_set(True)
        c = stdscr.getch()
        curses.curs_set(False)

        if c in [ord("q"), ord("Q")]:
            break
        elif c == curses.KEY_RESIZE:
            pass  # TODO fix resize crashing
        elif c in [curses.KEY_UP]:
            y = (y - 1) % args.rows
        elif c in [curses.KEY_DOWN]:
            y = (y + 1) % args.rows
        elif c in [curses.KEY_LEFT]:
            x = (x - 1) % args.cols
        elif c in [curses.KEY_RIGHT]:
            x = (x + 1) % args.cols
        elif c in [ord(" ")]:
            grid.flag(y, x) or grid.chord(y, x, auto=args.auto)
        elif c in [curses.KEY_ENTER, ord("\n"), ord("\r")]:
            grid.reveal(y, x, auto=args.auto)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plays a game of minesweeper")
    parser.add_argument("rows", help="number of rows", type=int)
    parser.add_argument("cols", help="number of columns", type=int)
    parser.add_argument("mines", help="number of mines", type=int)
    parser.add_argument("--lives", help="number of lives", type=int, default=1)
    parser.add_argument(
        "--no-color",
        help="disables colorful output",
        action="store_false",
        dest="color",
    )
    parser.add_argument(
        "--no-auto",
        help="disables automatic '0' propagation",
        action="store_false",
        dest="auto",
    )

    args = parser.parse_args()
    curses.wrapper(main, args)
