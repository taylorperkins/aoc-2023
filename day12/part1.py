from __future__ import annotations

from typing import List

from utils import getInput, timeit


def space_needed(damaged_springs: List[int]):
    if not damaged_springs:
        return 0
    length = len(damaged_springs)
    size = sum(damaged_springs)
    if length == 1:
        return size
    else:
        return size + length - 1


def get_arrangements(spring_conditions: str, damaged_springs: List[int], position: int):
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
            arrangements += get_arrangements(spring_conditions, rest, position+current_spring+1)

        if spring_conditions[position] == "#":
            break

        position += 1
    return arrangements


@timeit
def main(aoc: str):
    lines = aoc.splitlines()

    arrangements = 0

    for line in lines:
        spring_conditions, damaged_springs, *rest = line.split(" ")
        damaged_springs = [int(v) for v in damaged_springs.split(",")]

        n_arrangements = get_arrangements(spring_conditions, damaged_springs, 0)
        # print(f"{spring_conditions} | {damaged_springs} | {n_arrangements} | {rest}")
        if rest:
            assert n_arrangements == int(rest[0]), \
                f"{n_arrangements} does not equal {int(rest[0])}"
        arrangements += n_arrangements

    print(arrangements)


if __name__ == "__main__":
    # main(getInput("./input-test.txt"))
    # main(getInput("./input-test-2.txt"))
    main(getInput("./input.txt"))
