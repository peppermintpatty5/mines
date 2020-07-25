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
            raise ValueError("too many mines for grid size")

    def __str__(self):
        lose = len(self.dug & self.mines) >= self.lives
        return "\n".join(
            " ".join(
                "@"
                if (r, c) in self.dug and (r, c) in self.mines
                else "^"
                if (r, c) in self.flags and (r, c) in self.mines
                else ("X" if lose else "^")
                if (r, c) in self.flags
                else ("*" if lose else "-")
                if (r, c) in self.mines
                else str(len(adjacent(r, c) & self.mines))
                if (r, c) in self.dug
                else "-"
                for c in range(self.cols)
            )
            for r in range(self.rows)
        )

    def dig(self, r, c, auto=True):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            raise IndexError("grid index out of range")

        if len(self.mines) != self.nMines:  # Generate minefield
            self.mines = set(
                sample(
                    set(product(range(self.rows), range(self.cols))) - {(r, c)},
                    self.nMines,
                )
            )

        if (r, c) in self.dug:  # Uncover adjacent cells (chord)
            a = adjacent(r, c)
            s = a - self.flags if len(a & self.flags) == len(a & self.mines) else set()
        else:
            s = {(r, c)} if (r, c) not in self.flags else set()

        while len(s) != 0:
            r, c = s.pop()
            if 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in self.dug:
                a = adjacent(r, c)
                if auto and (r, c) not in self.mines and len(a & self.mines) == 0:
                    s.update(a - self.flags)
                self.dug.add((r, c))

    def flag(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            raise IndexError("grid index out of range")

        if (r, c) in self.flags:
            self.flags.remove((r, c))
        elif (r, c) not in self.dug:
            self.flags.add((r, c))


if __name__ == "__main__":
    m = Minesweeper(16, 30, 99)
    while True:
        try:
            opt = input("Enter 'd' to dig or 'f' to flag: ")
            if opt.lower() == "d" or opt.lower() == "f":
                r = int(input("Enter row: "))
                c = int(input("Enter col: "))
                m.dig(r, c, auto=True) if opt.lower() == "d" else m.flag(r, c)
                print(str(m).replace("0", " "))
            else:
                raise ValueError(f"invalid option '{opt}'")
        except (ValueError, IndexError) as e:
            print(e)
            pass
        except KeyboardInterrupt as e:
            print("")
            pass
        except EOFError as e:
            print("Exiting...")
            break
