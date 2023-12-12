from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from typing import Tuple, List

from utils import getInput, timeit


Coord = Tuple[int, int]


def dist(l: Coord, r: Coord) -> int:
    return abs(l[0] - r[0]) + abs(l[1] - r[1])


@timeit
def main(aoc: str):
    lines = aoc.splitlines()

    galaxies: List[Coord] = []

    # defaults to false -
    x_empty = [True] * len(lines)
    y_empty = [True] * len(lines[0])

    for x, row in enumerate(lines):
        for y, col in enumerate(row):
            if col == "#":
                galaxies.append((x, y,))
                x_empty[x] = False
                y_empty[y] = False

    # how much to increment per index
    x_inc = [sum(x_empty[:i]) for i in range(len(lines))]
    y_inc = [sum(y_empty[:i]) for i in range(len(lines[0]))]

    # re-map galaxy coords
    galaxies = [
        (x + x_inc[x], y + y_inc[y])
        for x, y in galaxies
    ]

    shortest_paths = [
        dist(g1, g2)
        for g1, g2 in combinations(galaxies, 2)
    ]

    print(sum(shortest_paths))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
