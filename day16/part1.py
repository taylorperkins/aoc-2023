from __future__ import annotations

from collections import defaultdict
from typing import List, Tuple, Callable, Dict

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


def energize(tiles: Matrix) -> int:
    visited: Dict[Tuple[Coord, Traversal], bool] = defaultdict(bool)
    shape = len(tiles), len(tiles[0])

    def traverse(directions: List[Tuple[Coord, Traversal]]) -> None:
        """BFS until can't go any further"""
        if not directions:
            return

        _next: List[Tuple[Coord, Traversal]] = []
        for c, d in directions:
            if coord_is_valid(c, shape) and not visited[(c, d,)]:
                visited[(c, d)] = True
                value = tiles[c[0]][c[1]]
                # print(f"{c} {value} | {d.__name__}")

                if value == ".":
                    _next.append((d(c), d,))
                else:
                    for next_d in TRAVERSAL_OPTIONS[(value, d,)]:
                        _next.append((next_d(c), next_d))

        return traverse(_next)

    traverse([((0, 0,), right)])
    return len({key[0] for key in visited.keys()})


@timeit
def main(aoc: str):
    tiles = [
        list(line)
        for line in aoc.splitlines()
    ]

    print(energize(tiles))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
