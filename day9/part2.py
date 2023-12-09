from functools import reduce
from typing import List

from utils import getInput, timeit


def get_differences(row: List[int]):
    return [
        v - row[idx]
        for idx, v in enumerate(row[1:])
    ]


def get_next_history(history: List[int]):
    diffs = [history]
    diff = history
    while sum(diff) != 0:
        diff = get_differences(diff)
        diffs.append(diff)

    return reduce(
        lambda v, row: row[0] - v,
        diffs[::-1],
        0
    )


@timeit
def main(aoc: str):
    rows = (
        [int(v) for v in line.split(" ")]
        for line in aoc.splitlines()
    )

    out = sum(get_next_history(row) for row in rows)
    print(out)


if __name__ == "__main__":
    main(getInput("./input-test-2.txt"))
    main(getInput("./input.txt"))

