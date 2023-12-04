from utils import getInput

valid_digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_digits(line: str):
    for i in range(len(line) + 1):
        for k, v in valid_digits.items():
            if line[:i].endswith(k) or line[:i].endswith(v):
                yield v


def main(aoc: str):
    acc = 0
    for line in aoc.splitlines():
        digits = list(get_digits(line))
        first = 0
        last = len(digits)-1
        acc += int(digits[first] + digits[last])

    print(acc)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
