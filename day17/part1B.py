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


TRAVERSAL_OPTIONS: Dict[Traversal, Tuple[Traversal, Traversal]] = {
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

    def __init__(
        self,
        _map: Matrix,
        shape: Coord,
        coord: Coord,
        direction: Optional[Traversal] = None,
        cumulative_cost: int = 0,
        parent: Optional[Node] = None,
    ):
        self.parent = parent
        # total cost of all parents leading up to here
        self.cumulative_cost = cumulative_cost
        # how did you get to here? Start should always be None, but
        # children should have a value
        self.direction = direction
        self.coord = coord
        self.map = _map
        self._shape = shape

        self.value = _map[self.coord[0]][self.coord[1]]
        self.distance = manhattan(self.coord, (shape[0]-1, shape[1]-1,))

    def __eq__(self, other):
        if isinstance(other, tuple):
            return other == self.coord
        return self.id == other.hash

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Node({self.coord})"

    @property
    def id(self):
        coords = [self.coord]
        for p in self.parents(2):
            if p.direction != self.direction:
                break
            coords.append(p.coord)
        return tuple(coords)

    def H(self):
        return self.value + self.distance

    def G(self):
        return self.cumulative_cost - self.value

    def cost(self, closed_nodes: Set[Node]):
        return self.G() + self.H()

    def neighbor_cost(self, closed_nodes: Set[Node]):
        costs = []
        for d in self.next_directions:
            c = d(self.coord)
            if coord_is_valid(c, self._shape) and c not in closed_nodes:
                costs.append(self.map[c[0]][c[1]]*manhattan(c, (self._shape[0]-1, self._shape[1]-1,)))
        return min(costs, default=0)

    @property
    def direction_cost(self):
        # bottom right is the target, and we can't reverse, so let's
        # penalize going up or going left by 1
        return 2 if self.direction in (up, left,) else 1

    def parents(self, depth: int = 0):
        if self.parent is not None:
            yield self.parent
            if depth == 1:
                return
            yield from self.parent.parents(depth=depth-1)

    @property
    def next_directions(self) -> List[Traversal]:
        if self.direction is None:
            return [left, right, up, down]

        sides = TRAVERSAL_OPTIONS[self.direction]
        n_same_directions = sum(p.direction == self.direction for p in self.parents(2))
        if n_same_directions < 2:
            sides += (self.direction,)

        return list(sides)


def min_path(_map: Matrix) -> Node:
    shape = len(_map), len(_map[0])
    target = shape[0]-1, shape[1]-1
    start = Node(_map=_map, shape=shape, coord=(0, 0,))

    # k: coord associated with the node
    # v: the number of times the node has been visited from a single direction, up to 3
    #    - we don't really care about parents if they came from a different direction
    closed_nodes = defaultdict(set)
    open_nodes: Set[Node] = {start}

    while open_nodes:
        current_node = min(open_nodes, key=lambda n: n.cost(closed_nodes.keys()))
        open_nodes.remove(current_node)

        if current_node.coord == target:
            return current_node

        # number of times we've come this same direction
        n_previous_directions = 1
        for p in current_node.parents(2):
            if p.direction == current_node.direction:
                n_previous_directions += 1

        closed_nodes[current_node.coord].add(current_node.id)

        for d in current_node.next_directions:
            next_coord = d(current_node.coord)
            if coord_is_valid(next_coord, shape):
                value = _map[next_coord[0]][next_coord[1]]
                node = Node(
                    _map=_map,
                    shape=shape,
                    coord=next_coord,
                    direction=d,
                    parent=current_node,
                    cumulative_cost=current_node.cumulative_cost + value
                )
                if node.id not in closed_nodes[node.coord]:
                    open_nodes.add(node)


@timeit
def main(aoc: str):
    _map: Matrix = [
        [int(v) for v in line]
        for line in aoc.splitlines()
    ]

    node = min_path(_map)
    print(node.cumulative_cost)

    grid = np.zeros((len(_map), len(_map[0])), dtype=int)
    grid[node.coord[0]][node.coord[1]] = 1
    for p in node.parents():
        grid[p.coord[0]][p.coord[1]] = 1

    print(grid)
    print(_map[node.coord[0]][node.coord[1]] + sum(_map[p.coord[0]][p.coord[1]] for p in node.parents()) - _map[0][0])

    # out = min_path(_map)
    # print(out.history)
    # print(out.value)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    # 683 - too high
    # main(getInput("./input.txt"))
