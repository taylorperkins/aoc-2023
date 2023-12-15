from __future__ import annotations

import abc
from enum import Enum, auto
from typing import List, Type

from utils import getInput, timeit


# list of list for in-place item assignment.. Naughty!
Matrix = List[List[str]]


class Direction(str, Enum):
    FORWARD = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Operation(metaclass=abc.ABCMeta):
    def __init__(self, matrix: Matrix):
        self._matrix = matrix
        self._shape = (len(self._matrix), len(self._matrix[0]))

    @property
    @abc.abstractmethod
    def targets(self) -> Matrix:
        pass

    @abc.abstractmethod
    def pure(self, idx: int) -> int:
        """Return a 'pure' version of idx based on the direction you're going"""
        pass

    @property
    @abc.abstractmethod
    def size(self) -> int:
        pass

    @property
    def rows(self) -> List[List[str]]:
        return self._matrix

    @property
    def columns(self) -> List[List[str]]:
        return [self.column(idx) for idx in range(self._shape[1])]

    def row(self, idx) -> List[str]:
        return self._matrix[idx]

    def column(self, idx) -> List[str]:
        return [row[idx] for row in self.rows]

    @staticmethod
    def factory(direction: Direction) -> Type[Operation]:
        if direction == Direction.FORWARD:
            return Forward

    def swap_values(self, this: (int, int), that: (int, int)):
        lx, ly = self.pure(this[0]), self.pure(this[1])
        rx, ry = self.pure(that[0]), self.pure(that[1])
        self._matrix[lx][ly], self._matrix[rx][ry] = self._matrix[rx][ry], self._matrix[lx][ly]

    @abc.abstractmethod
    def swap(self, at: int, this: int, that: int): pass


class Forward(Operation):
    def swap(self, at: int, this: int, that: int):
        self.swap_values((this, at), (that, at))

    @property
    def size(self) -> int:
        return self._shape[0]

    def pure(self, idx: int) -> int:
        return idx

    @property
    def targets(self) -> Matrix:
        return self.columns


class Backward(Operation):
    def swap(self, at: int, this: int, that: int):
        self.swap_values((this, at), (that, at))

    @property
    def size(self) -> int:
        return self._shape[0]

    def pure(self, idx: int) -> int:
        return self._shape[0] - idx

    @property
    def targets(self) -> Matrix:
        return self.columns


class Right(Operation):
    def swap(self, at: int, this: int, that: int):
        self.swap_values((at, this), (at, that))

    @property
    def size(self) -> int:
        return self._shape[1]

    def pure(self, idx: int) -> int:
        return self._shape[1] - idx

    @property
    def targets(self) -> Matrix:
        return self.columns


class Left(Operation):
    def swap(self, at: int, this: int, that: int):
        self.swap_values((at, this), (at, that))

    @property
    def size(self) -> int:
        return self._shape[1]

    def pure(self, idx: int) -> int:
        return idx

    @property
    def targets(self) -> Matrix:
        return self.columns


# anticipating having to tilt in multiple directions for pt. 2
def tilt(m: Matrix, d: Direction):
    """'Tilt' the matrix in the given direction.
    Start at a side and work towards the other side, swapping values
    as necessary.
    """
    op = Operation.factory(d)(m)

    for idx, t in enumerate(op.targets):
        s = 0
        for p in range(op.size):
            v = t[op.pure(p)]
            if v == ".":
                s += 1
            elif v == "#":
                s = 0
            else:
                # swap
                op.swap(idx, p, p-s)

    return m


@timeit
def main(aoc: str):
    m: Matrix = [
        list(line)
        for line in aoc.splitlines()
    ]

    m = tilt(m, Direction.FORWARD)

    size = len(m)
    print(sum([
        sum(size - idx for v in row if v == "O")
        for idx, row in enumerate(m)
    ]))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
