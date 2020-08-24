from itertools import product
from random import sample


class Grid:
    """Single-use game of minesweeper"""

    def __init__(self, rows, cols, mines):
        kwargs = {"rows": rows, "cols": cols, "mines": mines}
        for k, v in kwargs.items():
            if type(v) is not int or v < 0:
                raise TypeError(f"'{k}' must be non-negative integer")
        if mines > rows * cols - 1:
            raise ValueError(f"too many mines (limit {rows * cols - 1})")

        self.__rows = rows
        self.__cols = cols
        self.__numMines = mines
        self.__revealed = set()
        self.__flags = set()
        self.__mines = set()

    def __contains__(self, x):
        try:
            r, c = x
            return r in range(self.__rows) and c in range(self.__cols)
        except Exception as e:
            return False

    def __getitem__(self, x):
        R, F, M = self.__revealed, self.__flags, self.__mines
        if x not in self:
            raise ValueError("invalid row/col")

        return (
            "@"
            if x in R and x in M
            else "#"
            if x in F and x in M
            else "X"
            if x in F
            else "*"
            if x in M
            else str(len(self.__adjacent(*x) & M))
            if x in R
            else "-"
        )

    def __str__(self):
        return "\n".join(
            " ".join(self[(r, c)] for c in range(self.__cols))
            for r in range(self.__rows)
        )

    def __adjacent(self, r, c):
        A = set(product({r - 1, r, r + 1}, {c - 1, c, c + 1})) - {(r, c)}

        return {t for t in A if t in self}

    def __generate(self, r, c):
        self.__mines |= set(
            sample(
                set(product(range(self.__rows), range(self.__cols))) - {(r, c)},
                self.__numMines,
            )
        )

    def __autoReveal(self, s0):
        R, F, M = self.__revealed, self.__flags, self.__mines

        S = set(s0)
        while len(S) != 0:
            x = S.pop()
            A = self.__adjacent(*x)
            if x not in M and len(A & M) == 0:
                S |= A - R - F
            R |= {x}

    def reveal(self, r, c, auto=True):
        x, R, F, M = (r, c), self.__revealed, self.__flags, self.__mines
        if x not in self:
            raise ValueError("invalid row/col")

        if len(M) != self.__numMines:
            self.__generate(*x)

        if x not in F:
            R |= {x}

            if auto:
                self.__autoReveal({x})
            return True
        else:
            return False

    def flag(self, r, c):
        x, R, F, M = (r, c), self.__revealed, self.__flags, self.__mines
        if x not in self:
            raise ValueError("invalid row/col")

        if x not in R:
            F ^= {x}

            return True
        else:
            return False

    def chord(self, r, c, auto=True):
        x, R, F, M = (r, c), self.__revealed, self.__flags, self.__mines
        if x not in self:
            raise ValueError("invalid row/col")

        A = self.__adjacent(*x)
        if x in R and x not in M and len(A & F) + len(A & R & M) == len(A & M):
            R |= A - F

            if auto:
                self.__autoReveal(A - F)
            return True
        else:
            return False
