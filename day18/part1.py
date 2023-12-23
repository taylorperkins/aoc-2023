from __future__ import annotations

from collections import defaultdict
from typing import Tuple, Callable, List
from shapely import Point, Polygon

from utils import getInput, timeit


Coord = Tuple[int, int]
Traversal = Callable[[Coord], Coord]


def left(p: Point) -> Point:
    return Point(p.x, p.y-1)


def right(p: Point) -> Point:
    return Point(p.x, p.y+1)


def up(p: Point) -> Point:
    return Point(p.x-1, p.y)


def down(p: Point) -> Point:
    return Point(p.x+1, p.y)


TRAVERSAL_MAP = {
    "R": right,
    "L": left,
    "U": up,
    "D": down,
}


@timeit
def main(aoc: str):
    grid: List[Point] = [Point(0, 0,)]

    # x: Set[y]
    range_map = defaultdict(set)

    for line in aoc.splitlines():
        direction, amount, color = line.split(" ")
        amount = int(amount)
        # color = color[1:-1]
        direction = TRAVERSAL_MAP[direction]

        current = grid[-1]
        for _ in range(amount):
            current = direction(current)
            range_map[current.xr].add(current.yr)
            grid.append(current)

    poly = Polygon(grid)
    print((poly.area) + len(grid)-1)
    # interior_size = 0
    # for x, ys in range_map.items():
    #     for y in range(int(min(ys)), int(max(ys))+1):
    #         if poly.contains(Point(x, y)):
    #             interior_size += 1

    # print(len(grid)-1+interior_size)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
