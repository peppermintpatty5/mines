#!/usr/bin/env python3

from itertools import product
from random import sample
from time import clock
from sys import argv


class Minesweeper:
    """Single-use game of minesweeper"""

    def __init__(self, rows, cols, mines, lives=1):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.lives = lives
        self.__r = set()
        self.__f = set()
        self.__m = set()

    def __str__(self):
        lose = self.lose()
        return "\n".join(
            " ".join(
                "@"
                if (r, c) in self.__r and (r, c) in self.__m
                else "^"
                if (r, c) in self.__f and (r, c) in self.__m
                else ("X" if lose else "^")
                if (r, c) in self.__f
                else ("*" if lose else "-")
                if (r, c) in self.__m
                else str(len(Minesweeper.__adjacent(r, c) & self.__m))
                if (r, c) in self.__r
                else "-"
                for c in range(self.cols)
            )
            for r in range(self.rows)
        )

    @staticmethod
    def __adjacent(*t):
        return set(product(*((n - 1, n, n + 1) for n in t))) - {tuple(t)}

    def __generate(self, r, c):
        self.__m = set(
            sample(
                set(product(range(self.rows), range(self.cols))) - {(r, c)}, self.mines,
            )
        )

    def lose(self):
        return len(self.__r & self.__m) >= self.lives

    def win(self):
        return (
            not self.lose()
            and len(self.__r - self.__m) == self.rows * self.cols - self.mines
        )

    def primaryClick(self, r, c, auto=True):
        if len(self.__m) != self.mines:
            self.__generate(r, c)

        a = Minesweeper.__adjacent(r, c)
        if (r, c) not in self.__r:
            s = {(r, c)} if (r, c) not in self.__f else set()
        else:
            s = a - self.__f if len(a & self.__f) == len(a & self.__m) else set()

        while len(s) != 0:
            r, c = s.pop()
            if 0 <= r < self.rows and 0 <= c < self.cols and (r, c) not in self.__r:
                a = Minesweeper.__adjacent(r, c)
                if auto and (r, c) not in self.__m and len(a & self.__m) == 0:
                    s.update(a - self.__f)
                self.__r.add((r, c))

    def secondaryClick(self, r, c):
        if (r, c) in self.__f:
            self.__f.remove((r, c))
        elif (r, c) not in self.__r:
            self.__f.add((r, c))


if __name__ == "__main__":
    # This section of code is hideous, might fix it later

    kwargs, keys = {}, ["rows", "cols", "mines", "lives"]
    for a in argv[1:]:
        try:
            for i, t in enumerate(keys):
                if a.startswith(f"-{t}="):
                    kwargs[t] = int(a.split("=")[1])
                    break
                elif i == len(keys) - 1:
                    raise TypeError()
        except:
            print(f"Invalid argument '{a}'")
            exit()
    for k, v in kwargs.items():
        if v < 0:
            print(f"'{k}' cannot be negative")
            exit()
    try:
        if kwargs["mines"] > kwargs["rows"] * kwargs["cols"] - 1:
            print("Too many mines")
            exit()
    except Exception as e:
        print(f"Missing argument for {e}")
        exit()

    mode = 1  # click mode (primary/secondary)
    m = Minesweeper(**kwargs)
    while True:
        try:
            r = input(f"row{'>' * mode} ")
            if r == "":
                mode = 1 if mode == 2 else 2
                continue
            else:
                r = int(r)
            c = input(f"col{'>' * mode} ")
            if c == "":
                mode = 1 if mode == 2 else 2
                continue
            else:
                c = int(c)

            if 0 <= r < m.rows and 0 <= c < m.cols:
                m.primaryClick(r, c) if mode == 1 else m.secondaryClick(r, c)
                print(str(m).replace("0", " "))
                if m.lose():
                    print("YOU LOSE!")
                    exit()
                if m.win():
                    print("YOU WIN!")
                    exit()
            else:
                raise IndexError("Invalid index")
        except (ValueError, IndexError) as e:
            print(e)
            pass
        except KeyboardInterrupt as e:
            print("")
            pass
        except EOFError as e:
            print("Exiting...")
            break
