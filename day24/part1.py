from __future__ import annotations

from dataclasses import dataclass
import dataclasses
import itertools
import math
from typing import List, Tuple, Optional

from utils import getInput, timeit


Coord = Tuple[float, float]
Line = Tuple[Coord, Coord]


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
    def xy(self):
        return self.px, self.py

    def move(self, nanoseconds: int = 1) -> Hailstone:
        return dataclasses.replace(
            self,
            px=self.px + (self.vx * nanoseconds),
            py=self.py + (self.vy * nanoseconds),
            pz=self.pz + (self.vz * nanoseconds),
        )

    def xy_distance(self, other: Hailstone):
        return math.sqrt(sum([
            (self.px - other.px) ** 2,
            (self.py - other.py) ** 2
        ]))

    def angle(self, base: Line) -> float:
        assert self.xy in base
        # we want the connecting coord to be in the middle (c2)
        c1, c2 = base if base[1] == self.xy else base[::-1]
        c3 = self.move(1).xy

        u = (c1[0] - c2[0], c1[1] - c2[1])
        v = (c3[0] - c2[0], c3[1] - c2[1])

        # Calculate dot product and vector magnitudes
        dot_product = u[0] * v[0] + u[1] * v[1]
        magnitude_u = math.sqrt(u[0] ** 2 + u[1] ** 2)
        magnitude_v = math.sqrt(v[0] ** 2 + v[1] ** 2)

        # Calculate cosine of the angle
        cos_theta = dot_product / (magnitude_u * magnitude_v)

        # Calculate angle in radians
        angle_rad = math.acos(cos_theta)

        # Convert angle to degrees
        angle_deg = math.degrees(angle_rad)

        return angle_deg

    def intersecting_point(self, other: Hailstone) -> Optional[Coord]:
        base: Line = (self.xy, other.xy)
        la, ra = self.angle(base), other.angle(base)
        print(f"{self}: {la}")
        print(f"{other}: {ra}")

        if la + ra == 180:
            print("Parallel")
            return None

        if la + ra > 180:
            print("Crossed in the past")
            return None

        base_length = self.xy_distance(other)
        vertex_angle = 180 - la - ra
        print(vertex_angle)

        # figure out the distance from self to the vertex
        # - law of sines
        distance = (base_length*math.sin(ra))/math.sin(vertex_angle)
        slope = self.vy/self.vx

        # Calculate change in x and change in y
        delta_x = distance / math.sqrt(1 + slope ** 2)
        delta_y = slope * delta_x

        print(f"Will cross at {self.px+delta_x, self.py+delta_y}")
        return self.px+delta_x, self.py+delta_y


@timeit
def main(aoc: str):
    hailstones: List[Hailstone] = []

    for line in aoc.splitlines():
        pos, vel = line.split(" @ ")
        pos = (int(v.strip()) for v in pos.split(","))
        vel = (int(v.strip()) for v in vel.split(","))

        hailstones.append(Hailstone(*pos, *vel))

    for l, r in itertools.combinations(hailstones, 2):
        l: Hailstone
        r: Hailstone

        print()
        intersecting_point = l.intersecting_point(r)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))

    # main(getInput("./input.txt"))
