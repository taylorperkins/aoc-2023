from __future__ import annotations

from collections import defaultdict
from typing import Callable, Dict, List, Tuple

from utils import getInput, timeit


def hash_value(s: str, acc: int = 0):
    if not s:
        return acc

    c = s[0]
    acc += ord(c)
    acc *= 17
    acc %= 256

    return hash_value(s[1:], acc)


def split(s: str, fn: Callable[[str], bool], acc: str = "") -> (str, str):
    if not s:
        return acc, ''
    _next = s[0]
    if fn(_next):
        return acc, s
    return split(s[1:], fn, acc + _next)


@timeit
def main(aoc: str):
    hashmap: Dict[int, List[Tuple[str, int]]] = defaultdict(list)
    for step in aoc.split(","):
        label, rest = split(step, lambda s: not s.isalpha())
        box_number = hash_value(label)

        operation = rest[0]
        if operation == '-':
            hashmap[box_number] = [
                v for v in hashmap[box_number]
                if v[0] != label
            ]

        elif operation == '=':
            focal_length = int(rest[1:])
            existing_focal_lengths = (
                i for i, v in enumerate(hashmap[box_number])
                if v[0] == label
            )

            try:
                idx = next(existing_focal_lengths)
            # wasn't found
            except StopIteration:
                hashmap[box_number].append((label, focal_length))
            else:
                hashmap[box_number][idx] = (label, focal_length)

    score = sum(
        (box_number+1)*(idx+1)*focal_number
        for box_number, box in hashmap.items()
        for idx, (_, focal_number) in enumerate(box)
    )
    print(score)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
