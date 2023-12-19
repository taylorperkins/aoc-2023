from __future__ import annotations

import pickle
from collections import defaultdict
from typing import Tuple, Callable, List
from shapely import Point, Polygon

from utils import getInput, timeit


Coord = Tuple[int, int]
Traversal = Callable[[Coord], Coord]


def left(p: Point, amount: int = 1) -> Point:
    return Point(p.x, p.y-amount)


def right(p: Point, amount: int = 1) -> Point:
    return Point(p.x, p.y+amount)


def up(p: Point, amount: int = 1) -> Point:
    return Point(p.x-amount, p.y)


def down(p: Point, amount: int = 1) -> Point:
    return Point(p.x+amount, p.y)


TRAVERSAL_MAP = {
    "0": right,
    "2": left,
    "3": up,
    "1": down,
}


@timeit
def main(aoc: str):
    grid: List[Point] = [Point(0, 0,)]

    for line in aoc.splitlines():
        _, _, color = line.split(" ")
        amount = int(color[2:7], 16)
        direction = TRAVERSAL_MAP[color[-2]]

        current = grid[-1]
        current = direction(current, amount)
        grid.append(current)

    poly = Polygon(grid)
    with open("./poly.pkl", "wb") as f:
        pickle.dump(poly, f)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    # main(getInput("./input.txt"))
