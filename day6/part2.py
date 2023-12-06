import math

from utils import getInput, timeit


def calc_distance(max_time: int, speed: int):
    return (max_time-speed)*speed


def calc_speed(max_time: int, distance: int):
    """Given `Distance = Speed("Max Time" - Speed)`,
    you can re-write in standard form of a quadratic
    equation for Speed.

    Speed^2 - Speed*Time + Distance = 0

    Solve for speed using the quadratic formula, substituting
    coefficients from above.

    a = 1, b = -Time, c = Distance
    """
    # There are two possible outcomes, so account for both
    z = math.sqrt(max_time**2-distance*4)
    return (max_time-z)/2, (max_time+z)/2


@timeit
def main(aoc: str):
    times, distances = aoc.splitlines()
    t = int(times[5:].replace(" ", ""))
    d = int(distances[9:].replace(" ", ""))

    optimal_speed = t // 2
    current_distance = calc_distance(t, optimal_speed)
    i = 0
    while current_distance > d:
        i += 1
        current_distance = calc_distance(t, optimal_speed-i)

    # when even, there is a peak in the distanceXtime distribution,
    # so account for the peak.
    if t % 2 == 0:
        n_wins = (i-1)*2+1
    # when odd, it's mirrored
    else:
        n_wins = i*2

    print(n_wins)


@timeit
def main_v2(aoc: str):
    times, distances = aoc.splitlines()
    t = int(times[5:].replace(" ", ""))
    d = int(distances[9:].replace(" ", ""))

    min_s, _ = calc_speed(t, d)
    # we only need one speed to calc the overall number of wins.
    s = math.floor(min_s)+1
    left_n_wins = (t // 2) - s + 1

    # when even, there is a peak in the distanceXtime distribution,
    # so account for the peak.
    if t % 2 == 0:
        n_wins = (left_n_wins-1)*2+1
    # when odd, it's mirrored
    else:
        n_wins = left_n_wins*2

    print(n_wins)


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
    main_v2(getInput("./input.txt"))
