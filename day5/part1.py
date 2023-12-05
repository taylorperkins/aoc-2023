from functools import reduce
from typing import List

from utils import getInput, timeit


class CategoryMap:
    def __init__(self, source: int, destination: int, step: int):
        self.source = range(source, source+step)
        self.destination = range(destination, destination+step)

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


@timeit
def main(aoc: str):
    components = aoc.split("\n\n")
    seeds = [int(seed) for seed in components[0][7:].split(" ")]

    maps = []
    for c in components[1:]:
        category_maps = []
        for line in c.splitlines()[1:]:
            destination, source, step = [
                int(v) for v in line.split(" ")
            ]
            category_maps.append(CategoryMap(
                source=source,
                destination=destination,
                step=step
            ))
        maps.append(Map(category_maps=category_maps))

    destination_values = [
        reduce(
            lambda v, m: m[v],
            maps,
            seed
        )
        for seed in seeds
    ]

    print(min(destination_values))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
