#!/usr/bin/env python3

from mines import Grid
import argparse
import curses


def printGrid(stdscr, grid, color, colorMap, r0, c0, r1, c1):
    cellColors = {
        "1": "BRIGHT BLUE",
        "2": "GREEN",
        "3": "BRIGHT RED",
        "4": "BLUE",
        "5": "RED",
        "6": "CYAN",
        "7": "BRIGHT WHITE",
        "8": "BRIGHT BLACK",
        "@": "BRIGHT YELLOW",
        "*": "YELLOW",
        "#": "BRIGHT GREEN",
        "X": "BRIGHT MAGENTA",
        "-": "WHITE",
    }
    lose = False  # TODO need win/lose function
    hide = {"X": "#", "*": "-"}
    maxY, maxX = stdscr.getmaxyx()

    for r in range(r0, r1):
        for c in range(c0, c1):
            x, y = c * 2 + 1, r
            cell = grid[(r, c)]

            if not lose:
                cell = hide[cell] if cell in hide else cell

            if cell == "0":
                cell = " "

            if x < maxX and y < maxY:
                stdscr.addch(
                    y,
                    x,
                    cell,
                    colorMap[cellColors[cell]]
                    if color and cell in cellColors
                    else curses.color_pair(0),
                )


def main(stdscr, args):
    # curses init
    colorKeys = [
        "BLACK",
        "RED",
        "GREEN",
        "YELLOW",
        "BLUE",
        "MAGENTA",
        "CYAN",
        "WHITE",
        "BRIGHT BLACK",
        "BRIGHT RED",
        "BRIGHT GREEN",
        "BRIGHT YELLOW",
        "BRIGHT BLUE",
        "BRIGHT MAGENTA",
        "BRIGHT CYAN",
        "BRIGHT WHITE",
    ]
    colorMap = {}
    curses.use_default_colors()

    if curses.COLORS >= 16:
        for i, I in enumerate(colorKeys):
            if i != 0:
                curses.init_pair(i, i, -1)
            colorMap[I] = curses.color_pair(i) | curses.A_NORMAL
    elif curses.COLORS >= 8:
        for i, I in enumerate(colorKeys):
            if i != 0 and i < 8:
                curses.init_pair(i, i, -1)
            colorMap[I] = curses.color_pair(i % 8) | (
                curses.A_NORMAL if i < 8 else curses.A_BOLD
            )

    # game init
    r, c = 0, 0
    r0, c0, r1, c1 = 0, 0, args.rows, args.cols  # TODO grid viewing rectangle
    grid = Grid(args.rows, args.cols, args.mines)

    # game loop
    while True:
        maxY, maxX = stdscr.getmaxyx()
        printGrid(stdscr, grid, args.color, colorMap, r0, c0, r1, c1)

        stdscr.move(r, 2 * c + 1)  # TODO can crash if cursor moves out of display
        curses.curs_set(1)
        stdscr.refresh()
        ch = stdscr.getch()
        curses.curs_set(0)

        if ch in [ord("q"), ord("Q")]:
            break
        elif ch in [curses.KEY_UP]:
            r = (r - 1) % args.rows
        elif ch in [curses.KEY_DOWN]:
            r = (r + 1) % args.rows
        elif ch in [curses.KEY_LEFT]:
            c = (c - 1) % args.cols
        elif ch in [curses.KEY_RIGHT]:
            c = (c + 1) % args.cols
        elif ch in [ord(" ")]:
            grid.flag(r, c) or grid.chord(r, c, auto=args.auto)
        elif ch in [curses.KEY_ENTER, ord("\n"), ord("\r")]:
            grid.reveal(r, c, auto=args.auto)


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
