import re

from utils import getInput


digits_ptrn = re.compile(r'\d+')


def score(numbers, value: int = 0):
    if len(numbers) == 0:
        return value
    elif value == 0:
        return score(numbers[1:], 1)
    else:
        return score(numbers[1:], value*2)


def main(aoc: str):
    scores = []

    for line in aoc.splitlines():
        card_id, numbers = line.split(":")
        winning_numbers, numbers_i_have = numbers.split("|")
        winning_numbers = {int(d) for d in digits_ptrn.findall(winning_numbers)}
        numbers_i_have = {int(d) for d in digits_ptrn.findall(numbers_i_have)}

        chicken_dinner = numbers_i_have.intersection(winning_numbers)
        scores.append(score(list(chicken_dinner)))

    print(sum(scores))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
