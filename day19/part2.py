from __future__ import annotations

import re
from queue import Queue
from typing import Dict, Tuple, List

from utils import getInput, timeit


def lt(this: int, that: int):
    return this < that


def gt(this: int, that: int):
    return this > that


# key, range, like range(1, 4000)
Ratings = Dict[str, range]
# key, condition, limit, destination
Rule = Tuple[str, str, int, str]


def split_rating(rating: range, condition: str, limit: int):
    """Split the rating into two new ranges.
    The first range is matching the condition and limit, and the
    second is outside of the condition."""
    if condition == "<":
        l = range(rating.start, limit-1)
        r = range(limit, rating.stop)
    else:
        l = range(limit+1, rating.stop)
        r = range(rating.start, limit)

    return (
        l if l.start <= l.stop else None,
        r if r.start <= r.stop else None
    )


class Workflow:
    def __init__(self, _id: str, rules: List[Rule], fallback: str):
        self.id = _id
        self.rules = rules
        self.fallback = fallback


def get_combinations(ratings: Ratings, workflows: Dict[str, Workflow]) -> int:
    q = Queue()
    q.put((workflows["in"], ratings))

    accepted = []
    while not q.empty():
        wf, r = q.get()
        wf: Workflow
        r: Ratings

        current = r.copy()
        for (rating_key, condition, limit, destination) in wf.rules:
            _range = current[rating_key]
            success, failure = split_rating(_range, condition, limit)

            current = dict(current, **{rating_key: failure})

            if success is not None:
                if destination == "A":
                    accepted.append(dict(current, **{rating_key: success}))
                elif destination != "R":
                    q.put((workflows[destination], dict(current, **{rating_key: success})))

        if wf.fallback == "A":
            accepted.append(current)
        elif wf.fallback != "R":
            q.put((workflows[wf.fallback], current))

    score = 0
    for ratings in accepted:
        rating_score = 1
        for _range in ratings.values():
            rating_score *= (_range.stop-_range.start+1)
        score += rating_score

    return score


@timeit
def main(aoc: str):
    raw_workflows, raw_part_ratings = aoc.split("\n\n")

    workflow_ptrn = re.compile(r'(?P<name>\w+)\{(?P<rules>.*)}')
    rule_ptrn = re.compile(r'(?P<key>\w+)(?P<condition>[<|>])(?P<limit>\d+):(?P<destination>\w+)')

    workflows = {}

    for line in raw_workflows.splitlines():
        m = workflow_ptrn.match(line)
        workflow_name, raw_rules = m.group("name"), m.group("rules")
        *crs, f = raw_rules.split(",")
        rules: List[Rule] = []
        for cr in crs:
            m = rule_ptrn.match(cr)
            rules.append((
                m.group("key"),
                m.group("condition"),
                int(m.group("limit")),
                m.group("destination"),
            ))
        workflows[workflow_name] = Workflow(workflow_name, rules, f)

    ratings = {
        "x": range(1, 4000),
        "m": range(1, 4000),
        "a": range(1, 4000),
        "s": range(1, 4000),
    }

    print(get_combinations(ratings, workflows))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
