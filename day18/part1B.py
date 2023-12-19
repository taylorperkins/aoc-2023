from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import chain
from typing import Tuple, Callable, List, Dict, Generator, Optional, Set
from shapely import Point, Polygon

from utils import getInput, timeit


Coord = Tuple[int, int]
# inclusive, pls
_Range = Coord
Traversal = Callable[[Coord], Coord]


def left(p: Point, amount: int = 1) -> Point:
    return Point(p.x, p.y-amount)


def right(p: Point, amount: int = 1) -> Point:
    return Point(p.x, p.y+amount)


def up(p: Point, amount: int = 1) -> Point:
    return Point(p.x-amount, p.y)


def down(p: Point, amount: int = 1) -> Point:
    return Point(p.x+amount, p.y)


TRAVERSAL_MAP = {
    "R": right,
    "L": left,
    "U": up,
    "D": down,
}


def intersection(r1: range, r2: range):
    return range(
        max(r1.start, r2.start),
        min(r1.stop, r2.stop)
    )


def intersects(r1: range, r2: range):
    return intersection(r1, r2) or None


def split_at(r1: range, r2: range) -> Generator[range]:
    xs = sorted({r1.start, r1.stop, r2.start, r2.stop})
    for i in range(len(xs) - 1):
        start, stop = xs[i], xs[i + 1]
        if (start, stop) != (r2.start, r2.stop):
            yield range(start, stop)


@dataclass
class Range:
    i: int
    label: str

    # start/stop is inclusive
    range: range

    def __hash__(self):
        return hash((self.i, self.range,))

    def __eq__(self, other):
        return self.i == other.i and self.label == other.label and self.range == other.range


def merge_ranges(ranges: List[Range]):
    sorted_ranges = sorted(ranges, key=lambda r: (r.i, r.range.start))
    current_range = sorted_ranges.pop(0)
    for r in sorted_ranges:
        if current_range.i != r.i:
            yield current_range
            current_range = r

        elif current_range.range.start <= r.range.start <= current_range.range.stop:
            current_range = Range(
                current_range.i,
                label=current_range.label,
                range=range(current_range.range.start, r.range.stop))

        else:
            yield current_range
            current_range = r
    yield current_range


@timeit
def main(aoc: str):
    line: List[Point] = [Point(0, 0,)]

    horizontal_ranges: Dict[int, List[Range]] = defaultdict(list)
    vertical_ranges: Dict[int, List[Range]] = defaultdict(list)

    corners: Set[Coord] = set()
    for row in aoc.splitlines():
        direction_symbol, amount, color = row.split(" ")
        amount = int(amount)
        # color = color[1:-1]
        direction = TRAVERSAL_MAP[direction_symbol]

        current_point = line[-1]
        corners.add((current_point.x, current_point.y))
        next_point = direction(current_point, amount)
        line.append(next_point)
        if direction_symbol in ["U", "D"]:
            xs = sorted([current_point.x, next_point.x])
            vertical_ranges[int(current_point.y)].append(Range(
                i=int(current_point.y),
                label="V",
                range=range(int(xs[0]), int(xs[1]))
            ))
        else:
            ys = sorted([current_point.y, next_point.y])
            horizontal_ranges[int(current_point.x)].append(Range(
                i=int(current_point.x),
                label="H",
                range=range(int(ys[0]), int(ys[1]))
            ))

    # idea is that you start on the far left, and continue to break down
    # connecting ranges to create rectangles. From there, determine the inner
    # area, and note the horizontal edges
    vertical_ranges = {i: list(merge_ranges(r)) for i, r in vertical_ranges.items()}

    # start with the vertical area (lines, inclusive of ends)
    score = sum(
        abs(r.range.start-r.range.stop)-1
        for i, ranges in vertical_ranges.items()
        for r in ranges
    )

    vertical_ranges: List[Range] = list(chain(*[
        vertical_ranges[k]
        for k in sorted(vertical_ranges.keys())
    ]))

    while vertical_ranges:
        # leftmost range
        left_range = vertical_ranges.pop(0)
        right_range_idx = vertical_ranges.index(next(r for r in vertical_ranges if intersects(r.range, left_range.range)))
        right_range = vertical_ranges.pop(right_range_idx)

        intersection_range = intersection(left_range.range, right_range.range)

        area = abs(right_range.i-left_range.i+1)*abs(intersection_range.stop-intersection_range.start+1)
        perimeter = abs(right_range.i-left_range.i)*2 + abs(intersection_range.stop-intersection_range.start)*2
        interior_area = area - perimeter
        score += interior_area

        # note inclusive
        r = range(left_range.i, right_range.i)
        if r:
            # top
            horizontal_ranges[intersection_range.start].append(
                Range(i=intersection_range.start, label="H", range=r)
            )
            # bottom
            horizontal_ranges[intersection_range.stop].append(
                Range(i=intersection_range.stop, label="H", range=r)
            )

        for r in split_at(right_range.range, intersection_range):
            vertical_ranges.insert(right_range_idx, Range(right_range.i, right_range.label, r))

        for r in split_at(left_range.range, intersection_range):
            vertical_ranges.insert(0, Range(left_range.i, left_range.label, r))

    horizontal_ranges = {i: list(merge_ranges(r)) for i, r in horizontal_ranges.items()}

    corner_score = 0
    for c in corners:
        valid = True
        for r in horizontal_ranges[c[0]]:
            if r.range.start < c[1] < r.range.stop:
                valid = False
        if valid:
            corner_score += 1

    score += corner_score

    horizontal_score = 0
    for idx, ranges in horizontal_ranges.items():
        for r in ranges:
            v = abs(r.range.start - r.range.stop) - 1
            horizontal_score += v

    score += horizontal_score
    print(score)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
