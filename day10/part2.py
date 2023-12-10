from __future__ import annotations

from typing import Tuple, Dict, Set, List, Callable, Generator

from shapely import Point, Polygon

from utils import getInput, timeit

Coord = Tuple[int, int]

NODES: Dict[Node, Set[Node]] = {}


def left(coord: Coord) -> Coord:
    return coord[0], coord[1] - 1


def right(coord: Coord) -> Coord:
    return coord[0], coord[1] + 1


def up(coord: Coord) -> Coord:
    return coord[0] - 1, coord[1]


def down(coord: Coord) -> Coord:
    return coord[0] + 1, coord[1]


class Graph:

    def __init__(self, _map: List[List[str]]):
        global NODES
        NODES = {}

        self.shape = len(_map), len(_map[0])
        self.map = _map

        self._pipe_directions: Dict[str, List[Callable[[Coord], Coord]]] = {
            "S": [left, right, up, down],
            "|": [up, down],
            "-": [left, right],
            "L": [up, right],
            "J": [up, left],
            "7": [down, left],
            "F": [down, right],
        }

        for i, row in enumerate(_map):
            for j, val in enumerate(row):
                self.add(Node((i, j), val))

    def __getitem__(self, coord: Coord) -> Node:
        return Node(
            coord=coord,
            value=self.map[coord[0]][coord[1]]
        )

    def clear(self):
        NODES = {}

    def within_bounds(self, coord: Coord):
        return 0 <= coord[0] < self.shape[0] and 0 <= coord[1] < self.shape[1]

    def add(self, node: Node):
        if node in NODES:
            raise RuntimeError("Node already exists in the graph")

        NODES[node] = set()
        if self.within_bounds(node.coord):
            for fn in self._pipe_directions.get(node.value, []):
                coord = fn(node.coord)
                if self.within_bounds(coord):
                    NODES[node].add(self[coord])

    def find(self, fn: Callable[[Node], bool]) -> Generator[Node, None, None]:
        yield from (n for n in NODES.keys() if fn(n))

    def cycle_size(self, start: Node):

        next_nodes = {start}
        visited_nodes = set()
        i = 0

        while next_nodes:
            current_nodes = next_nodes
            visited_nodes = visited_nodes.union(current_nodes)

            next_nodes = set()
            for n in current_nodes:
                for a in n.adjacent:
                    if n.is_connected(a) and a not in visited_nodes:
                        next_nodes.add(a)

            if next_nodes:
                i += 1
        return i

    def cycle(self, start: Node) -> Generator[Node, None, None]:
        yield start

        connected_nodes = [n for n in start.adjacent if start.is_connected(n)]
        previous = start
        # ignoring direction, just choosing one.
        current = connected_nodes[0]
        while current != start:
            yield current
            connected_nodes = [
                n for n in current.adjacent
                if current.is_connected(n)
                   and n != previous
            ]
            # should only ever be one
            previous = current
            current = connected_nodes[0]

        yield start


class Node:
    def __init__(self, coord: Coord, value: str):
        self.coord = coord
        self.value = value

    @property
    def adjacent(self) -> Set[Node]:
        return NODES.get(self, set())

    def is_connected(self, other: Node):
        return other in self.adjacent and self in other.adjacent

    # allow comparison between different instances
    def __hash__(self):
        return hash((self.coord[0], self.coord[1], self.value,))

    def __eq__(self, other: Node):
        return self.value == other.value and self.coord == other.coord

    def __repr__(self):
        return f"Node({self.coord}, {self.value})"


@timeit
def main(aoc: str):
    graph = Graph([
        list(line)
        for line in aoc.splitlines()
    ])

    start = next(graph.find(lambda n: n.value == "S"))

    cycle_coords = [n.coord for n in graph.cycle(start)]
    poly = Polygon(cycle_coords)
    n_contained = sum(
        1
        for x in range(graph.shape[0])
        for y in range(graph.shape[1])
        if (x, y) not in cycle_coords
        and poly.contains(Point(x, y))
    )

    print(n_contained)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input-test-2.txt"))
    main(getInput("./input-test-3.txt"))
    main(getInput("./input-test-4.txt"))
    main(getInput("./input-test-5.txt"))
    main(getInput("./input.txt"))
