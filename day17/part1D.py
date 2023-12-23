from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional, Callable

from utils import getInput, timeit


Coord = Tuple[int, int]
Direction = Callable[[Coord], Coord]


def left(c: Coord) -> Coord:
    return c[0], c[1]-1


def right(c: Coord) -> Coord:
    return c[0], c[1]+1


def up(c: Coord) -> Coord:
    return c[0]-1, c[1]


def down(c: Coord) -> Coord:
    return c[0]+1, c[1]


REVERSE_DIRECTIONS = {
    left: right,
    right: left,
    up: down,
    down: up
}


def coord_is_valid(c: Coord, shape: Coord):
    return 0 <= c[0] < shape[0] and 0 <= c[1] < shape[1]


@dataclass
class Path:
    cost: int
    visited: List[Coord]
    recent_direction: Optional[Direction] = None
    recent_counter: int = 0

    def can_traverse(self, d: Direction) -> bool:
        out = True

        if d == REVERSE_DIRECTIONS.get(self.recent_direction):
            out = False
        elif d == self.recent_direction and self.recent_counter >= 3:
            out = False

        return out


@timeit
def main(aoc: str):
    grid = [
        [int(v) for v in line]
        for line in aoc.splitlines()
    ]

    start = 0, 0
    shape = len(grid), len(grid[0])
    end = shape[0]-1, shape[1]-1

    # accessing based on cost?
    paths: Dict[int, List[Path]] = defaultdict(list)
    paths[0].append(Path(0, [start]))

    closed_nodes: Dict[Coord, List[Tuple[int, Direction]]] = defaultdict(list)

    while paths:
        min_cost = min(paths)
        current_paths = paths.pop(min_cost)

        for current_path in current_paths:
            last_coord = current_path.visited[-1]
            if (current_path.recent_counter, current_path.recent_direction,) not in closed_nodes[last_coord]:
                closed_nodes[last_coord].append((current_path.recent_counter, current_path.recent_direction,))
                for d in (up, down, left, right):
                    if current_path.can_traverse(d):
                        next_coord = d(last_coord)
                        if coord_is_valid(next_coord, shape) and next_coord not in current_path.visited:
                            next_path = Path(
                                cost=current_path.cost + grid[next_coord[0]][next_coord[1]],
                                visited=current_path.visited + [next_coord],
                                recent_direction=d,
                                recent_counter=1 if d != current_path.recent_direction else current_path.recent_counter + 1
                            )

                            if next_coord == end:
                                print(next_path.cost)
                                return

                            if (next_path.recent_counter, next_path.recent_direction) not in closed_nodes:
                                paths[next_path.cost].append(next_path)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
