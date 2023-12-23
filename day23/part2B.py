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


@dataclass
class TrailHead:
    coord: Coord
    # connecting trail heads and the cost to go there
    trails: List[Tuple[Coord, int]]


def max_scenic_trail(trails: Dict[Coord, TrailHead], start: Coord, end: Coord) -> int:
    q = queue.Queue()
    q.put((trails[start], [start], 0))

    score = 0

    # while-loop b/c python sucks at recursion
    while not q.empty():
        (t, v, s) = q.get()
        t: TrailHead
        v: List[Coord]
        s: int

        for (c, cost) in t.trails:
            if c == end and s+cost > score:
                score = s+cost

            # treating v as a queue and checking the most recent should
            # speed up checking if you've visited it before, at least
            # in the case of long lines in the same direction.
            elif c != v[-1] and c not in v[:-1]:
                q.put((trails[c], v + [c], s+cost))

    return score


def get_connected_paths(c: Coord, shape: Coord, _map: List[str]) -> List[Coord]:
    return [
        nc
        for nc in get_neighbors(c)
        if coord_is_valid(nc, shape)
        and _map[nc[0]][nc[1]] != "#"
    ]


def get_next_trail_head(
    c: Coord,
    recent: Coord,
    trail_heads: List[Coord],
    _map: List[str],
    shape: Coord,
    score: int = 1
) -> Tuple[Coord, int]:
    if c in trail_heads:
        return c, score

    for p in get_connected_paths(c, shape, _map):
        if p != recent:
            return get_next_trail_head(p, c, trail_heads, _map, shape, score+1)


@timeit
def main(aoc: str):
    raw_trails = aoc.splitlines()
    shape = len(raw_trails), len(raw_trails[0])

    start = next((0, i) for i in range(shape[1]) if raw_trails[0][i] == ".")
    end = next((shape[0]-1, i) for i in range(shape[1]) if raw_trails[shape[0]-1][i] == ".")

    # a trail head is any path having 3 touching paths
    # in addition to the start and end, having only one neighbor
    trail_heads: List[Coord] = [start, end]

    for x, line in enumerate(raw_trails):
        for y, value in enumerate(line):
            c = x, y
            if value != "#":
                # we don't care if you step on an icy slope that goes back
                # to this node, it will get resolved later.
                paths = get_connected_paths(c, shape, raw_trails)
                if len(paths) >= 3:
                    trail_heads.append(c)

    trails: Dict[Coord, TrailHead] = {}
    for c in trail_heads:
        trails[c] = TrailHead(c, [
            get_next_trail_head(p, c, trail_heads, raw_trails, shape, 1)
            for p in get_connected_paths(c, shape, raw_trails)
        ])

    # for t in trails.values():
    #     print(t)

    print(max_scenic_trail(trails, start, end))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
