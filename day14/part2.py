from __future__ import annotations

import abc
from collections import defaultdict
from enum import Enum, auto
from typing import List, Type

from utils import getInput, timeit


# list of list for in-place item assignment.. Naughty!
Matrix = List[List[str]]


class Direction(str, Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


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

    def swap_values(self, this: (int, int), that: (int, int)):
        lx, ly = self.pure(this[0]), self.pure(this[1])
        rx, ry = self.pure(that[0]), self.pure(that[1])
        self._matrix[lx][ly], self._matrix[rx][ry] = self._matrix[rx][ry], self._matrix[lx][ly]

    @abc.abstractmethod
    def swap(self, at: int, this: int, that: int): pass


class North(Operation):
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


class South(Operation):
    def swap(self, at: int, this: int, that: int):
        self.swap_values((this, at), (that, at))

    @property
    def size(self) -> int:
        return self._shape[0]

    def pure(self, idx: int) -> int:
        return self._shape[0] - idx - 1

    @property
    def targets(self) -> Matrix:
        return self.columns[::-1]


class East(Operation):
    def swap(self, at: int, this: int, that: int):
        self.swap_values((at, this), (at, that))

    @property
    def size(self) -> int:
        return self._shape[1]

    def pure(self, idx: int) -> int:
        return self._shape[1] - idx - 1

    @property
    def targets(self) -> Matrix:
        return self.rows[::-1]


class West(Operation):
    def swap(self, at: int, this: int, that: int):
        self.swap_values((at, this), (at, that))

    @property
    def size(self) -> int:
        return self._shape[1]

    def pure(self, idx: int) -> int:
        return idx

    @property
    def targets(self) -> Matrix:
        return self.rows


def tilt(m: Matrix, operation_cls: Type[Operation]):
    """'Tilt' the matrix in the given direction.
    Start at a side and work towards the other side, swapping values
    as necessary.
    """
    op = operation_cls(m)

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

    spin_cycle = [North, West, South, East]
    score_counter = defaultdict(list)
    size = len(m)

    i = 0
    limit = 1_000_000_000
    cycle_found = False
    while i < limit:
        for op in spin_cycle:
            m = tilt(m, op)

        score = 0
        text = []
        for idx, row in enumerate(m):
            score += (row.count("O") * (size-idx))
            text.append("".join(row))

        text = "\n".join(text)

        key = (score, text)
        score_counter[key].append(i)
        if not cycle_found and len(score_counter[key]) > 10:
            cycle_found = True
            first, second = score_counter[key][-2], score_counter[key][-1]
            idx_diff = second - first
            delta = idx_diff * ((limit - idx_diff - second) // idx_diff)
            i += delta

        i += 1
        if i == limit:
            print(score)
            break


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
