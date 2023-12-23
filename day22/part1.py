from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from itertools import chain
from typing import Set, Dict, List, Any

from utils import getInput, timeit


def ranges_intersect(l: range, r: range):
    # has to be a better way, but idk
    return (
        l.start <= r.start <= l.stop
        or l.start <= r.stop <= l.stop
        or r.start <= l.start <= r.stop
        or r.start <= l.stop <= r.stop
    )


@dataclass
class Brick:
    id: Any
    xr: range
    yr: range
    zr: range

    parents: Dict[Any, Brick] = field(default_factory=dict)
    children: Dict[Any, Brick] = field(default_factory=dict)

    def add_parent(self, other: Brick):
        self.parents[other.id] = other

    def add_child(self, other: Brick):
        self.children[other.id] = other

    @property
    def bottom(self):
        return self.zr.start

    @property
    def top(self):
        return self.zr.stop

    def xy_intersect(self, other: Brick):
        return ranges_intersect(self.xr, other.xr) and ranges_intersect(self.yr, other.yr)

    def z_shift(self, n: int):
        self.zr = range(self.zr.start + n, self.zr.stop + n)

    @property
    def hash(self):
        return hash((self.xr, self.yr, self.zr,))

    def __eq__(self, other: Brick):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash


@timeit
def main(aoc: str):
    z_bricks: Dict[int, Dict[Any, Brick]] = defaultdict(dict)
    bricks = []

    for (idx, line) in enumerate(aoc.splitlines()):
        l, r = line.split("~")
        l, r = l.split(","), r.split(",")
        xr = range(*sorted([int(l[0]), int(r[0])]))
        yr = range(*sorted([int(l[1]), int(r[1])]))
        zr = range(*sorted([int(l[2]), int(r[2])]))

        b = Brick(idx, xr, yr, zr)
        bricks.append(b)
        for i in range(zr.start, zr.stop+1):
            z_bricks[i][b.id] = b

    max_z = max(z_bricks.keys())
    # for i in range(max_z):
    #     print(f"{max_z-i}: {z_bricks[max_z-i]}")

    # no need to start on the bottom
    for z in range(2, max(z_bricks.keys())+1):
        current_brick_ids = [bid for bid, b in z_bricks[z].items() if b.bottom == z]
        for b_id in current_brick_ids:
            brick = z_bricks[z][b_id]

            next_level = z
            i = 0
            while True:
                i += 1
                lower_z = z-i
                if lower_z == 0:
                    break

                intersecting_bricks = (b for b in z_bricks[lower_z].values() if brick.xy_intersect(b))
                try:
                    # ran into another brick. Connect them, then go back up
                    b = next(intersecting_bricks)
                    b.add_child(brick)
                    brick.add_parent(b)

                    for b in intersecting_bricks:
                        b.add_child(brick)
                        brick.add_parent(b)

                    break

                # no bricks, can shift down
                except StopIteration:
                    next_level = lower_z
                    pass

            shift = brick.bottom - next_level
            if not shift:
                continue

            for bz in range(brick.zr.start, brick.zr.stop + 1):
                del z_bricks[bz][brick.id]

            brick.z_shift(-shift)

            for bz in range(brick.zr.start, brick.zr.stop + 1):
                z_bricks[bz][brick.id] = brick

    for i in range(max_z):
        print(f"{max_z-i}: {[b.id for b in z_bricks[max_z-i].values()]}")

    total = 0
    for brick in bricks:
        for child in brick.children.values():
            if len(child.parents) == 1:
                break
        else:
            total += 1

    print(total)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
