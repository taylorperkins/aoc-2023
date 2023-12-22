from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple, Callable, Optional, Dict, Set

import numpy as np

from utils import getInput, timeit


Matrix = List[List[int]]
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


def coord_is_valid(c: Coord, shape: Coord):
    return 0 <= c[0] < shape[0] and 0 <= c[1] < shape[1]


def manhattan(this: Coord, that: Coord) -> int:
    return abs(this[0] - that[0]) + abs(this[1] - that[1])


TRAVERSAL_OPTIONS: Dict[Traversal, Tuple[Traversal, Traversal]] = {
    left: (up, down,),
    right: (up, down,),
    up: (left, right,),
    down: (left, right,),
}
TRAVERSAL_SYMBOLS = {left: "<", right: ">", down: "v", up: "^"}
SYMBOL_TRAVERSALS = {"<": left, ">": right, "v": down, "^": up}


def get_next_directions(history: str):
    if not history:
        return left, right, up, down

    directions = TRAVERSAL_OPTIONS[SYMBOL_TRAVERSALS[history[-1]]]

    # you can continue moving in the same direction if the past
    # three aren't the same
    if history[-3:] != history[-1]*3:
        directions += (SYMBOL_TRAVERSALS[history[-1]],)

    return directions


def take_while(value: str, fn: Callable[[str], bool]):
    for v in value:
        if fn(v):
            yield v
        else:
            break


def recent_same(history: str):
    return "".join(take_while(
        history[-3:][::-1],
        lambda v: v == history[-1]
    ))


@dataclass
class Node:
    coord: Coord
    history: str
    recent_history: str
    score: int
    target_distance: int
    center_distance: int


@timeit
def main(aoc: str):

    _map: Matrix = [
        [int(v) for v in line]
        for line in aoc.splitlines()
    ]

    shape = len(_map), len(_map[0])

    start = 0, 0
    target = shape[0]-1, shape[1]-1
    center = shape[0]//2, shape[1]//2
    recommended_center_distance = manhattan(start, center)

    # coord, history, score, distance
    open_nodes = [
        Node(
            coord=start,
            history="",
            recent_history="",
            score=0,
            target_distance=manhattan(start, target),
            center_distance=manhattan(start, center)
        )
    ]
    closed_nodes = []

    while open_nodes:
        # min score, order by distance
        # cn = current node
        # node: Node = min(open_nodes, key=lambda n: n.score + 1*(1*n.target_distance * 0.3*((recommended_center_distance-n.center_distance)/9)))
        node: Node = min(open_nodes, key=lambda n: n.score)
        if node.coord == target and node.score < 681:
            print(node.score, node.history)
            return

        open_nodes = [n for n in open_nodes if not (n.coord == node.coord and n.recent_history == node.recent_history)]
        closed_nodes.append((node.coord, node.recent_history))
        # closed_nodes.append(node.coord)

        for d in get_next_directions(node.history):
            next_coord = d(node.coord)
            symbol = TRAVERSAL_SYMBOLS[d]
            next_history = node.history + symbol
            next_recent_history = recent_same(next_history)

            # haven't visited under these conditions yet
            if coord_is_valid(next_coord, shape) and (next_coord, next_recent_history) not in closed_nodes:
                open_nodes.append(Node(
                    coord=next_coord,
                    history=next_history,
                    recent_history=next_recent_history,
                    score=node.score + _map[next_coord[0]][next_coord[1]],
                    target_distance=manhattan(next_coord, target),
                    center_distance=manhattan(next_coord, center)
                ))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    # 681, 682, 683 - too high
    # main(getInput("./input.txt"))
