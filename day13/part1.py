from collections import deque
from typing import List

from utils import getInput, timeit

Matrix = List[str]


def column(idx: int, m: Matrix) -> str:
    return "".join(r[idx] for r in m)


def row(idx: int, m: Matrix) -> str:
    return m[idx]


def transpose(m: Matrix) -> Matrix:
    return [
        column(idx, m)
        for idx in range(len(m[0]))
    ]


def row_before(idx: int, m: Matrix):
    return row(idx - 1, m)


def row_after(idx: int, m: Matrix):
    return row(idx + 1, m)


def forward(i: int):
    return i + 1


def reverse(i: int):
    return i - 1


def is_mirrored(first, second):
    return all([
        f == s
        for f, s in zip(first[::-1], second)
    ])


def calculate_default_score(m: Matrix):
    # doesn't consider row or column, just row
    center = len(m) // 2
    length = len(m)

    movement = deque([
        (center - 1, reverse, forward),
        (center + 1, forward, reverse),
    ])
    while movement:
        idx, _next, previous = movement.popleft()
        if not 0 <= idx < length:
            continue

        current_row, previous_row = row(idx, m), row(previous(idx), m)
        # potential mirror
        if current_row == previous_row:
            # we don't need to compare current and previous again,
            # just the next ones
            bottom, top = sorted([idx, previous(idx)])
            mirror_size = min([bottom + 1, length - top])

            l, r = m[bottom - mirror_size + 1:bottom], m[top + 1:top + mirror_size]
            if is_mirrored(l, r):
                return bottom + 1

        movement.append((_next(idx), _next, previous,))


def calculate_score(m: Matrix):
    row_score = calculate_default_score(m)
    if row_score is not None:
        return row_score * 100

    return calculate_default_score(transpose(m))


@timeit
def main(aoc: str):
    out = 0
    for _map in aoc.split("\n\n"):
        m = _map.splitlines()
        out += calculate_score(m)
    print(out)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
