import re
from functools import reduce
from math import floor

from utils import getInput, timeit


digits_ptrn = re.compile(r'\d+')

def calc_distance(max_time: int, speed: int):
    return (max_time-speed)*speed

@timeit
def main(aoc: str):
    times, distances = aoc.splitlines()
    times = (int(v) for v in digits_ptrn.findall(times[5:]))
    distances = (int(v) for v in digits_ptrn.findall(distances[9:]))

    n_wins = []
    for t, d in zip(times, distances):
        optimal_speed = t // 2
        current_distance = calc_distance(t, optimal_speed)
        i = 0
        while current_distance > d:
            i += 1
            current_distance = calc_distance(t, optimal_speed-i)

        # when even, there is a peak in the distanceXtime distribution,
        # so account for the peak.
        if t % 2 == 0:
            out = (i-1)*2+1
        # when odd, it's mirrored
        else:
            out = i*2

        n_wins.append(out)

    print(reduce(
        lambda x, y: x * y,
        n_wins, 1
    ))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
