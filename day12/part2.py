from __future__ import annotations

from functools import lru_cache
from typing import List, Tuple

from utils import getInput, timeit


def space_needed(damaged_springs: Tuple[int]):
    if not damaged_springs:
        return 0
    length = len(damaged_springs)
    size = sum(damaged_springs)
    if length == 1:
        return size
    else:
        return size + length - 1


@lru_cache(maxsize=None)
def get_arrangements(spring_conditions: str, damaged_springs: Tuple[int], position: int):
    # we skipped over a required position
    if position > 0 and spring_conditions[position-1:position] == "#":
        return 0

    # win condition
    if not damaged_springs and "#" not in spring_conditions[position:]:
        return 1

    # no more to go
    if not damaged_springs:
        return 0

    required_size = space_needed(damaged_springs)
    current_spring, *rest = damaged_springs

    arrangements = 0
    while required_size <= len(spring_conditions[position:]):
        if (
            "." not in spring_conditions[position:position+current_spring]
            and spring_conditions[position+current_spring:position+current_spring+1] != "#"
        ):
            arrangements += get_arrangements(spring_conditions, tuple(rest), position+current_spring+1)

        if spring_conditions[position] == "#":
            break

        position += 1
    return arrangements


@timeit
def main(aoc: str):
    lines = aoc.splitlines()

    arrangements = 0

    for idx, line in enumerate(lines):
        spring_conditions, damaged_springs, *rest = line.split(" ")
        damaged_springs = tuple(int(v) for v in damaged_springs.split(","))

        spring_conditions = "?".join([spring_conditions]*5)
        damaged_springs *= 5

        n_arrangements = get_arrangements(spring_conditions, damaged_springs, 0)
        # print(f"{spring_conditions} | {damaged_springs} | {n_arrangements} | {rest}")
        if rest:
            assert n_arrangements == int(rest[0]), \
                f"{n_arrangements} does not equal {int(rest[0])}"
        arrangements += n_arrangements

    print(arrangements)


if __name__ == "__main__":
    main(getInput("./input-test-3.txt"))
    main(getInput("./input.txt"))
