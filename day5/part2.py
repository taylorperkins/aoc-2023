from __future__ import annotations

from functools import reduce
from typing import List

from utils import getInput, timeit


class CategoryMap:
    def __init__(self, source: int, destination: int, step: int):
        self.source = range(source, source+step)
        self.destination = range(destination, destination+step)
        self._step = step

    def get(self, source: int):
        if self.source.start <= source < self.source.stop:
            return self.destination.start + (source - self.source.start)


class Map:
    def __init__(self, category_maps: List[CategoryMap], source: str = "", destination: str = ""):
        self.source = source
        self.destination = destination
        self.category_maps = category_maps

    # map
    def __getitem__(self, value: int):
        for cm in self.category_maps:
            dest = cm.get(value)
            if dest is not None:
                return dest
        return value


def get_seed_ranges(line):
    gen = (int(v) for v in line.split(" "))
    ranges = []
    while True:
        try:
            start, step = next(gen), next(gen)
        except StopIteration:
            return ranges
        else:
            ranges.append(range(start, start+step))


@timeit
def main(aoc: str):
    components = aoc.split("\n\n")

    maps = []
    for c in components[1:]:
        category_maps = []
        for line in c.splitlines()[1:]:
            destination, source, step = [
                int(v) for v in line.split(" ")
            ]
            category_maps.append(CategoryMap(
                source=destination,
                destination=source,
                step=step
            ))
        maps.append(Map(category_maps=category_maps))

    # reverse the process
    maps = maps[::-1]
    seed_ranges = get_seed_ranges(components[0][7:])

    i = 0
    iterations = 0
    target_seed = 0
    step = 100000

    while not target_seed:
        i += step
        iterations += 1
        # Going backwards from location
        seed = reduce(lambda v, m: m[v], maps, i)

        for r in seed_ranges:
            if r.start <= seed < r.stop:
                if step == 1:
                    target_seed = seed
                    break
                else:
                    # went too far, backoff and go slower
                    i -= step
                    step /= 10
                    break

    print(f"Location: {i}, seed: {target_seed}, iterations: {iterations}")


if __name__ == "__main__":
    # main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
