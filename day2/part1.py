import re

from utils import getInput

ptrn = re.compile(r'(?P<quantity>\d+)\s(?P<color>\w+)')
game_id_ptrn = re.compile(r'Game\s(\d+)')


game_rules = {
    "red": 12,
    "green": 13,
    "blue": 14
}


def is_possible(line):
    for game_set in line.split(";"):
        for quantity, color in ptrn.findall(game_set):
            if int(quantity) > game_rules[color]:
                return False
    return True


def main(aoc: str):
    possible = []

    for line in aoc.splitlines():
        if is_possible(line):
            game_id = int(
                game_id_ptrn
                .search(line)
                .group(1)
            )
            possible.append(game_id)

    print(sum(possible))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
