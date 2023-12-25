from __future__ import annotations

from dataclasses import dataclass
import dataclasses
import itertools
import math
from typing import List, Tuple, Optional

from utils import getInput, timeit


Coord = Tuple[float, float]
Line = Tuple[Coord, Coord]


def euclidean(l: Coord, r: Coord):
    return math.sqrt(sum([
        (l[0] - r[0]) ** 2,
        (l[1] - r[1]) ** 2
    ]))


@dataclass
class Hailstone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    def __repr__(self):
        return f"Hailstone({self.px}, {self.py}, {self.pz} @ {self.vx}, {self.vy}, {self.vz})"

    @property
    def xy_slope(self):
        return self.vy / self.vx

    @property
    def xy(self):
        return self.px, self.py

    def move(self, nanoseconds: int = 1) -> Hailstone:
        return dataclasses.replace(
            self,
            px=self.px + (self.vx * nanoseconds),
            py=self.py + (self.vy * nanoseconds),
            pz=self.pz + (self.vz * nanoseconds),
        )

    def intersecting_point(self, other: Hailstone) -> Optional[Coord]:
        if self.xy_slope == other.xy_slope:
            # print("Parallel")
            return None

        # all based on slope-point form, finding point of intersection
        # between two lines
        x = ((self.px*self.xy_slope) - (other.px*other.xy_slope) + other.py - self.py) / (self.xy_slope - other.xy_slope)
        # just need to solve for one side, should be the same
        y = self.xy_slope*(x-self.px) + self.py

        # moving closer
        if (
            euclidean(self.move(1).xy, (x, y)) <= euclidean(self.xy, (x, y))
            and euclidean(other.move(1).xy, (x, y)) <= euclidean(other.xy, (x, y))
        ):
            # print(f"Will cross at {x, y}")
            return x, y
        else:
            # print("Crossed in the past")
            return None


@timeit
def main(aoc: str, test_area: Coord):
    hailstones: List[Hailstone] = []

    for line in aoc.splitlines():
        pos, vel = line.split(" @ ")
        pos = (int(v.strip()) for v in pos.split(","))
        vel = (int(v.strip()) for v in vel.split(","))

        hailstones.append(Hailstone(*pos, *vel))

    i = 0
    for l, r in itertools.combinations(hailstones, 2):
        l: Hailstone
        r: Hailstone

        intersecting_point = l.intersecting_point(r)
        if (
            intersecting_point is not None
            and test_area[0] <= intersecting_point[0] <= test_area[1]
            and test_area[0] <= intersecting_point[1] <= test_area[1]
        ):
            i += 1

    print(i)


if __name__ == "__main__":
    main(getInput("./input-test.txt"), (7, 27))
    # 16244 - too high
    main(getInput("./input.txt"), (200000000000000, 400000000000000))
