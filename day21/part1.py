from __future__ import annotations

from collections import defaultdict
from typing import Tuple, Set, Dict

from utils import getInput, timeit


Coord = Tuple[int, int]


def left(c: Coord) -> Coord:
    return c[0], c[1]-1


def right(c: Coord) -> Coord:
    return c[0], c[1]+1


def up(c: Coord) -> Coord:
    return c[0]-1, c[1]


def down(c: Coord) -> Coord:
    return c[0]+1, c[1]


def neighbors(c: Coord):
    yield up(c)
    yield down(c)
    yield left(c)
    yield right(c)


def coord_is_valid(c: Coord, shape: Coord):
    return 0 <= c[0] < shape[0] and 0 <= c[1] < shape[1]



@timeit
def main(aoc: str):
    grid = [line for line in aoc.splitlines()]
    shape = len(grid), len(grid[0])

    plot_neighbors: Dict[Coord, Set[Coord]] = defaultdict(set)
    start = ...
    for x, line in enumerate(grid):
        for y, char in enumerate(line):
            c = x, y
            plot_neighbors[c] = {
                n for n in neighbors(c)
                if coord_is_valid(n, shape)
                and grid[n[0]][n[1]] != "#"
            }

            if char == "S":
                start = c

    current_plots = {start}
    for _ in range(64):
        next_plots = set()
        for c in current_plots:
            for n in plot_neighbors[c]:
                next_plots.add(n)
        current_plots = next_plots

    print(len(current_plots))


if __name__ == "__main__":
    # main(getInput("./input-test.txt"))
    # main(getInput("./input-test-2.txt"))
    main(getInput("./input.txt"))
