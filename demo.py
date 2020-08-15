#!/usr/bin/env python3

from mines import Grid
from sys import argv
import argparse
import curses


def printGrid(stdscr, grid):
    (
        BLACK,
        RED,
        GREEN,
        YELLOW,
        BLUE,
        MAGENTA,
        CYAN,
        WHITE,
        BRIGHT_BLACK,
        BRIGHT_RED,
        BRIGHT_GREEN,
        BRIGHT_YELLOW,
        BRIGHT_BLUE,
        BRIGHT_MAGENTA,
        BRIGHT_CYAN,
        BRIGHT_WHITE,
    ) = tuple(range(16))
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

    lose = False
    s = str(grid) if lose else str(grid).replace("X", "#").replace("*", "-")
    for row in s.split("\n"):
        stdscr.addstr(" ")
        for cell in row.split(" "):
            if cell != "0":
                stdscr.addstr(cell, curses.color_pair(cellColors[cell]))
            else:
                stdscr.addstr(" ")
            stdscr.addstr(" ")
        stdscr.addstr("\n")
    stdscr.refresh()


def main(stdscr, args):
    # curses init
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)

    # game init
    x, y = 0, 0
    grid = Grid(args.rows, args.cols, args.mines)

    # game loop
    while True:
        stdscr.move(0, 0)
        printGrid(stdscr, grid)
        stdscr.move(y, 2 * x + 1)

        curses.curs_set(True)
        c = stdscr.getch()
        curses.curs_set(False)
        if c in (ord("q"), ord("Q")):
            break
        elif c in [curses.KEY_UP, ord("w"), ord("W")]:
            y = (y - 1) % args.rows
        elif c in [curses.KEY_DOWN, ord("s"), ord("S")]:
            y = (y + 1) % args.rows
        elif c in [curses.KEY_LEFT, ord("a"), ord("A")]:
            x = (x - 1) % args.cols
        elif c in [curses.KEY_RIGHT, ord("d"), ord("D")]:
            x = (x + 1) % args.cols
        elif c in [ord(" ")]:
            grid.chord(y, x) or grid.flag(y, x)
        elif c in [curses.KEY_ENTER, ord("\n"), ord("\r")]:
            grid.reveal(y, x)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plays a game of minesweeper")
    parser.add_argument("rows", help="Number of rows", type=int)
    parser.add_argument("cols", help="Number of columns", type=int)
    parser.add_argument("mines", help="Number of mines", type=int)
    parser.add_argument("-l", "--lives", help="Number of lives", type=int, default=1)

    args = parser.parse_args()
    curses.wrapper(main, args)
