from itertools import product
from random import sample


class Grid:
    """Single-use game of minesweeper"""

    def __init__(self, rows, cols, mines, lives=1):
        kwargs = {"rows": rows, "cols": cols, "mines": mines, "lives": lives}
        for k, v in kwargs.items():
            if type(v) is not int or v < 0:
                raise TypeError(f"'{k}' must be non-negative integer")
        if mines > rows * cols - 1:
            raise ValueError("too many mines")

        self.__rows = rows
        self.__cols = cols
        self.__numMines = mines
        self.__numLives = lives
        self.__revealed = set()
        self.__flags = set()
        self.__mines = set()

    def __contains__(self, item):
        try:
            r, c = item
            return (
                int(r) == r
                and int(c) == c
                and 0 <= r < self.__rows
                and 0 <= c < self.__cols
            )
        except Exception as e:
            return False

    def __repr__(self):
        return ",\n".join(f"{k}: {v}" for k, v in self.__dict__.items())

    def __str__(self):
        R, F, M = self.__revealed, self.__flags, self.__mines
        lose = self.lose()
        return "\n".join(
            " ".join(
                "@"
                if (r, c) in R and (r, c) in M
                else "#"
                if (r, c) in F and (r, c) in M
                else ("X" if lose else "#")
                if (r, c) in F
                else ("*" if lose else "-")
                if (r, c) in M
                else str(len(self.__adjacent(r, c) & M))
                if (r, c) in R
                else "-"
                for c in range(self.__cols)
            )
            for r in range(self.__rows)
        )

    def __adjacent(self, r, c):
        return {
            x
            for x in product({r - 1, r, r + 1}, {c - 1, c, c + 1})
            if x in self and x != (r, c)
        }

    def __generate(self, r, c):
        self.__mines |= set(
            sample(
                set(product(range(self.__rows), range(self.__cols))) - {(r, c)},
                self.__numMines,
            )
        )

    def lose(self):
        return len(self.__revealed & self.__mines) >= self.__numLives

    def win(self):
        R, F, M = self.__revealed, self.__flags, self.__mines
        return (
            not self.lose()
            and len(R - M) == self.__rows * self.__cols - self.__numMines
        )

    def leftClick(self, r, c, auto=True):
        x = (r, c)
        R, F, M = self.__revealed, self.__flags, self.__mines
        if x not in self:
            raise ValueError("invalid row/col")

        if len(M) != self.__numMines:
            self.__generate(*x)

        A = self.__adjacent(*x)
        S = ({x} if x not in R else A if len(A & F) == len(A & M) else set()) - R - F

        while len(S) != 0:
            x = S.pop()
            A = self.__adjacent(*x)
            if auto and x not in M and len(A & M) == 0:
                S |= A - R - F
            R |= {x}

    def rightClick(self, r, c):
        x = (r, c)
        R, F, M = self.__revealed, self.__flags, self.__mines
        if x not in self:
            raise ValueError("invalid row/col")

        if x in F:
            F -= {x}
        elif x not in R:
            F |= {x}
