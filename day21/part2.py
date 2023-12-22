from __future__ import annotations

from collections import defaultdict
import json
from typing import Tuple, Dict, Callable, List

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


def cycle(v: int, max_: int):
    return v % max_


def translate_coord(c: Coord, shape: Coord):
    return c[0] % shape[0], c[1] % shape[1]


@timeit
def main(aoc: str):
    grid = [line for line in aoc.splitlines()]
    shape = len(grid), len(grid[0])

    plot_neighbors: Dict[Coord, List[Callable[[Coord], Coord]]] = defaultdict(list)
    start = ...
    for x, line in enumerate(grid):
        for y, char in enumerate(line):
            c = x, y
            for d in (up, down, left, right):
                n = d(c)
                t = translate_coord(n, shape)
                if grid[t[0]][t[1]] != "#":
                    plot_neighbors[c].append(d)

            if char == "S":
                start = c

    current_plots = {start}
    out = []
    elevens = defaultdict(list)
    for i in range(11*20):

        next_plots = set()
        for c in current_plots:
            for d in plot_neighbors[translate_coord(c, shape)]:
                next_plots.add(d(c))

        current_plots = next_plots
        out.append({"i": i, "n": len(current_plots)})
        elevens[i // 11].append(len(current_plots))

    # with open("./out.json", "w") as f:
    #     json.dump(out, f)

    with open("./pt2_test_prime.json", "w") as f:
        json.dump(elevens, f)

    print(len(current_plots))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    # main(getInput("./input-test-2.txt"))
    # main(getInput("./input.txt"))
