from __future__ import annotations

from collections import defaultdict
from functools import partial
from typing import List, Tuple, Callable, Dict, Generator

from utils import getInput, timeit


Matrix = List[List[str]]
Coord = Tuple[int, int]
Traversal = Callable[[Coord], Coord]


def left(c: Coord) -> Coord:
    return c[0], c[1]-1


def right(c: Coord) -> Coord:
    return c[0], c[1]+1


def up(c: Coord) -> Coord:
    return c[0]-1, c[1]


def down(c: Coord) -> Coord:
    return c[0]+1, c[1]


# (symbol, from): (to..,)
TRAVERSAL_OPTIONS = {
    ("-", left,): (left,),
    ("-", right,): (right,),
    ("-", up,): (left, right,),
    ("-", down,): (left, right,),
    ("|", left,): (up, down,),
    ("|", right,): (up, down,),
    ("|", up,): (up,),
    ("|", down,): (down,),
    ("/", left,): (down,),
    ("/", right,): (up,),
    ("/", up,): (right,),
    ("/", down,): (left,),
    ("\\", left,): (up,),
    ("\\", right,): (down,),
    ("\\", up,): (left,),
    ("\\", down,): (right,),
}


def coord_is_valid(c: Coord, shape: Coord):
    return 0 <= c[0] < shape[0] and 0 <= c[1] < shape[1]


def energize(start: Coord, direction: Traversal, tiles: Matrix, coord_validator: Callable[[Coord], Coord]) -> int:
    visited: Dict[Tuple[Coord, Traversal], bool] = defaultdict(bool)

    def traverse(directions: List[Tuple[Coord, Traversal]]) -> None:
        """BFS until can't go any further"""
        if not directions:
            return

        _next: List[Tuple[Coord, Traversal]] = []
        for c, d in directions:
            if coord_validator(c) and not visited[(c, d,)]:
                visited[(c, d)] = True
                value = tiles[c[0]][c[1]]
                # print(f"{c} {value} | {d.__name__}")

                if value == ".":
                    _next.append((d(c), d,))
                else:
                    for next_d in TRAVERSAL_OPTIONS[(value, d,)]:
                        _next.append((next_d(c), next_d))

        return traverse(_next)

    traverse([(start, direction)])
    return len({key[0] for key in visited.keys()})


def traversal_combinations(shape: Coord) -> Generator[(Coord, Traversal)]:
    # rows
    for i in range(shape[0]):
        yield (i, 0,), right
        yield (i, shape[1]-1,), left

    for i in range(shape[1]):
        yield (0, i,), down
        yield (shape[0]-1, i,), up


@timeit
def main(aoc: str):
    tiles = [
        list(line)
        for line in aoc.splitlines()
    ]

    shape = len(tiles), len(tiles[0])
    coord_validator: Callable[[Coord], Coord] = partial(coord_is_valid, shape=shape)

    optimal_energy = max(
        energize(start=c, direction=t, tiles=tiles, coord_validator=coord_validator)
        for c, t in traversal_combinations(shape)
    )

    print(optimal_energy)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
