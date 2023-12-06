from utils import getInput, timeit


def calc_distance(max_time: int, speed: int):
    return (max_time-speed)*speed

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


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
