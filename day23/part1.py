from __future__ import annotations

import queue
from dataclasses import dataclass
from typing import Tuple, List, Dict, Generator

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


def get_neighbors(c: Coord):
    for fn in (up, down, left, right):
        yield fn(c)


def coord_is_valid(c: Coord, shape: Coord):
    return 0 <= c[0] < shape[0] and 0 <= c[1] < shape[1]


SLOPE_NEIGHBORS = {">": right, "v": down, "<": left, "^": up}


@dataclass
class Trail:
    coord: Coord
    neighbors: List[Coord]


def max_scenic_trail(trails: Dict[Coord, Trail], start: Coord, end: Coord) -> int:
    q = queue.Queue()
    q.put((trails[start], [start], 0))

    score = 0

    # while-loop b/c python sucks at recursion
    while not q.empty():
        (t, v, s) = q.get()
        t: Trail
        v: List[Coord]
        s: int

        for n in t.neighbors:
            if n == end and s >= score:
                score = s+1
            # treating v as a queue and checking the most recent should
            # speed up checking if you've visited it before, at least
            # in the case of long lines in the same direction.
            elif n != v[-1] and n not in v[:-1]:
                q.put((trails[n], v + [n], s+1))

    return score


@timeit
def main(aoc: str):
    raw_trails = aoc.splitlines()
    shape = len(raw_trails), len(raw_trails[0])

    start = next((0, i) for i in range(shape[1]) if raw_trails[0][i] == ".")
    end = next((shape[0]-1, i) for i in range(shape[1]) if raw_trails[shape[0]-1][i] == ".")

    trails: Dict[Coord, Trail] = {}
    for x, line in enumerate(raw_trails):
        for y, value in enumerate(line):
            c = x, y
            if value == "#":
                continue
            elif value == ".":
                # we don't care if you step on an icy slope that goes back
                # to this node, it will get resolved later.
                neighbors = [
                    nc
                    for nc in get_neighbors(c)
                    if coord_is_valid(nc, shape)
                    and raw_trails[nc[0]][nc[1]] != "#"
                ]
                trails[c] = Trail(c, neighbors)
            # it's a slope, should have only one valid neighbor
            else:
                nc = SLOPE_NEIGHBORS[value](c)
                if coord_is_valid(nc, shape):
                    trails[c] = Trail(c, [nc])

    print(max_scenic_trail(trails, start, end))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
