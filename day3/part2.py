import re
from collections import defaultdict
from functools import reduce

from utils import getInput, timeit


def adjacent(row: int, start: int, stop: int):
    return (
        [(row-1, i) for i in range(start-1, stop+1)]
        + [(row, start-1), (row, stop)]
        + [(row+1, i) for i in range(start-1, stop+1)]
    )


def matrix_contains(shape, x, y):
    return 0 <= x < shape[0] and 0 <= y < shape[1]


ptrn = re.compile(r'(\d+)')


@timeit
def main(aoc: str):
    gears = defaultdict(list)

    matrix = aoc.splitlines()
    shape = len(matrix), len(matrix[0])

    for row_idx, line in enumerate(matrix):
        pos = 0
        while True:
            m = ptrn.search(line, pos)
            if not m:
                break

            value = int(m.group(0))
            start, pos = m.span(0)

            adj = adjacent(row_idx, start=start, stop=pos)
            adj = [(x, y) for x, y in adj if matrix_contains(shape, x=x, y=y)]
            for a_r, a_c in adj:
                if matrix[a_r][a_c] == "*":
                    gears[(a_r, a_c)].append(value)

    gear_ratios = [
        reduce(
            lambda x, y: x * y,
            part_numbers,
            1
        )
        for part_numbers in gears.values()
        if len(part_numbers) > 1
    ]

    print(sum(gear_ratios))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
