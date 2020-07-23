#!/usr/bin/env python3

from itertools import product
from random import sample


def adjacent(*t):
    return set(product(*((n - 1, n, n + 1) for n in t))) - {tuple(t)}


class Minesweeper:
    """Single-use game of minesweeper"""

    def __init__(self, rows, cols, nMines, lives=1):
        self.rows = abs(int(rows))
        self.cols = abs(int(cols))
        self.nMines = abs(int(nMines))
        self.lives = abs(int(lives))
        self.dug = set()
        self.flags = set()
        self.mines = set()
        if self.nMines > self.rows * self.cols - 1:
            raise ValueError("Too many mines for grid size")

    def __getitem__(self, index):
        r, c = index
        reveal = len(self.dug & self.mines) >= self.lives
        return (
            "@"
            if (r, c) in self.dug and (r, c) in self.mines
            else "^"
            if (r, c) in self.flags and (r, c) in self.mines
            else "^X"[reveal]
            if (r, c) in self.flags
            else "-*"[reveal]
            if (r, c) in self.mines
            else str(len(adjacent(r, c) & self.mines))
            if (r, c) in self.dug
            else "-"
        )

    def __str__(self):
        return "\n".join(
            " ".join(self[(r, c)] for c in range(self.cols)) for r in range(self.rows)
        ).replace("0", " ")

    def dig(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in self.flags:
            if self.dug == set():  # Generate the minefield on first click
                self.mines = set(
                    sample(
                        set(product(range(self.rows), range(self.cols))) - {(r, c)},
                        self.nMines,
                    )
                )

            s = set()
            if (r, c) in self.dug:  # Uncover adjacent cells (chord)
                a = adjacent(r, c)
                if len(a & self.flags) == len(a & self.mines):
                    s = a - self.flags
            else:
                s = {(r, c)}

            while len(s) > 0:
                r, c = s.pop()
                if 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in self.dug:
                    adj = adjacent(r, c)
                    f, m = len(adj & self.flags), len(adj & self.mines)
                    if (r, c) not in self.mines and (f == m or m == 0):
                        s.update(adj - self.flags)
                    self.dug.add((r, c))

    def flag(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if (r, c) in self.flags:
                self.flags.remove((r, c))
            elif (r, c) not in self.dug:
                self.flags.add((r, c))


if __name__ == "__main__":
    m = Minesweeper(16, 30, 99)
    while True:
        try:
            opt = input("Enter 'd' to dig or 'f' to flag: ").lower()
            if opt == "d" or opt == "f":
                r = int(input("Enter row: "))
                c = int(input("Enter col: "))
                (m.flag if opt == "f" else m.dig)(r, c)
                print(m)
        except ValueError as e:
            pass
        except EOFError as e:
            print("Exiting...")
            break
