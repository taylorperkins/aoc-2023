from __future__ import annotations

from utils import getInput, timeit


def hash_value(s: str, acc: int = 0):
    if not s:
        return acc

    c = s[0]
    acc += ord(c)
    acc *= 17
    acc %= 256

    return hash_value(s[1:], acc)


@timeit
def main(aoc: str):
    print(sum(
        hash_value(step)
        for step in aoc.split(",")
    ))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
