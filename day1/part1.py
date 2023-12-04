from utils import getInput


def main(aoc: str):
    acc = 0
    for line in aoc.splitlines():
        digits = [char for char in line if char.isdigit()]
        last = digits.pop()
        if not digits:
            first = last
        else:
            first = digits[0]
        acc += int(first + last)
    print(acc)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
