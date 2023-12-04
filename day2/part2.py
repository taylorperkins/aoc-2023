import re
from functools import reduce

from utils import getInput

ptrn = re.compile(r'(?P<quantity>\d+)\s(?P<color>\w+)')


def power_set(line):
    power = {}

    for game_set in line.split(";"):
        for quantity, color in ptrn.findall(game_set):
            if power.get(color, 0) < int(quantity):
                power[color] = int(quantity)

    return reduce(
        lambda x, y: x * y,
        power.values(),
        1
    )


def main(aoc: str):
    power = sum(
        power_set(line)
        for line in aoc.splitlines()
    )

    print(power)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
