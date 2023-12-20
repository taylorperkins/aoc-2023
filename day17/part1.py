from __future__ import annotations

import itertools
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple, Callable

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


TRAVERSAL_OPTIONS = {
    left: (up, down,),
    right: (up, down,),
    up: (left, right,),
    down: (left, right,),
}


def coord_is_valid(c: Coord, shape: Coord):
    return 0 <= c[0] < shape[0] and 0 <= c[1] < shape[1]


def manhattan(this: Coord, that: Coord) -> int:
    return abs(this[0] - that[0]) + abs(this[1] - that[1])


TRAVERSAL_SYMBOLS = {left: "<", right: ">", down: "v", up: "^"}
SYMBOL_TRAVERSALS = {"<": left, ">": right, "v": down, "^": up}


@dataclass
class Node:
    coord: Coord
    history: str
    value: int
    distance: int

    @property
    def symbol(self):
        return TRAVERSAL_SYMBOLS[self.direction]

    @property
    def opportunity_cost(self):
        return self.value + self.distance

    @property
    def direction(self):
        return SYMBOL_TRAVERSALS[self.history[-1]]

    @property
    def recent_history(self):
        return self.history[-3:]


def min_path(_map: Matrix):
    shape = len(_map), len(_map[0])
    target = shape[0]-1, shape[1]-1

    open_nodes = defaultdict(list)
    open_nodes[(0, 1,)].append(Node(coord=(0, 1,), history=">", value=_map[0][1], distance=manhattan((0, 1,), target)))
    open_nodes[(1, 0,)].append(Node(coord=(1, 0,), history="v", value=_map[1][0], distance=manhattan((1, 0,), target)))

    closed_nodes = []
    while open_nodes:
        current_node = min(
            itertools.chain(*open_nodes.values()),
            key=lambda n: n.opportunity_cost
        )
        open_nodes[current_node.coord] = [
            node
            for node in open_nodes[current_node.coord]
            if node.recent_history != current_node.recent_history
        ]
        closed_nodes.append(current_node.coord)

        directions = TRAVERSAL_OPTIONS[current_node.direction]
        if len(current_node.history) < 3:
            directions += (current_node.direction,)
        elif len(set(current_node.history[-3:])) != 1:
            directions += (current_node.direction,)

        for d in directions:
            c = d(current_node.coord)
            if coord_is_valid(c, shape):
                value = _map[c[0]][c[1]]

                candidate = Node(
                    coord=c,
                    history=current_node.history + TRAVERSAL_SYMBOLS[d],
                    value=current_node.value+value,
                    distance=manhattan(c, target)
                )

                if c == target:
                    return candidate

                if candidate.coord not in closed_nodes:
                    open_nodes[candidate.coord].append(candidate)


@timeit
def main(aoc: str):
    _map: Matrix = [
        [int(v) for v in line]
        for line in aoc.splitlines()
    ]

    out = min_path(_map)
    print(out.history)
    print(out.value)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    # 683 - too high
    main(getInput("./input.txt"))
