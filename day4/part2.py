import re
from collections import defaultdict

from utils import getInput, timeit

digits_ptrn = re.compile(r'\d+')


@timeit
def main(aoc: str):
    n_scratchcards = defaultdict(int)

    for idx, line in enumerate(aoc.splitlines()):
        game_id = idx+1
        n_scratchcards[game_id] += 1

        card_id, numbers = line.split(":")
        winning_numbers, numbers_I_have = numbers.split("|")

        winning_numbers = set(digits_ptrn.findall(winning_numbers))
        numbers_I_have = set(digits_ptrn.findall(numbers_I_have))

        intersect = numbers_I_have.intersection(winning_numbers)

        for i in range(len(intersect)):
            next_id = i + 1 + game_id
            n_scratchcards[next_id] += n_scratchcards[game_id]

    print(sum(n_scratchcards.values()))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
