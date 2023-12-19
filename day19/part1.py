from __future__ import annotations

import abc
import re
from typing import Callable, Dict, List

from utils import getInput, timeit


def lt(this: int, that: int):
    return this < that


def gt(this: int, that: int):
    return this > that


class Rule(metaclass=abc.ABCMeta):
    def __init__(self, value: str):
        self.value = value

    @abc.abstractmethod
    def __call__(self, value: Dict[str, int]) -> bool: pass


class ComparisonRule(Rule):
    def __init__(self, key: str, operator: str, comparable: int, value: str):
        super(ComparisonRule, self).__init__(value=value)
        self.key = key
        self.fn: Callable[[int, int], bool] = lt if operator == "<" else gt
        self.comparable = comparable

    def __call__(self, value: Dict[str, int]):
        return self.fn(value[self.key], self.comparable)


class FallbackRule(Rule):
    def __call__(self, value: Dict[str, int]):
        return True


class Workflow:
    def __init__(self, rules: List[Rule], fallback: str):
        self.rules = rules
        self.rules.append(FallbackRule(fallback))

    def __call__(self, value: Dict[str, int]) -> str:
        outputs = (r.value for r in self.rules if r(value))
        return next(outputs)


workflow_ptrn = re.compile(r'(?P<name>\w+)\{(?P<rules>.*)}')
rule_ptrn = re.compile(r'(?P<key>\w+)(?P<operator>[<|>])(?P<comparable>\d+):(?P<value>\w+)')


@timeit
def main(aoc: str):
    raw_workflows, raw_part_ratings = aoc.split("\n\n")

    workflows = {}
    for line in raw_workflows.splitlines():
        m = workflow_ptrn.match(line)
        workflow_name, raw_rules = m.group("name"), m.group("rules")
        *crs, f = raw_rules.split(",")
        comparison_rules = []
        for cr in crs:
            m = rule_ptrn.match(cr)
            comparison_rules.append(
                ComparisonRule(
                    key=m.group("key"),
                    operator=m.group("operator"),
                    comparable=int(m.group("comparable")),
                    value=m.group("value"),
                )
            )
        workflows[workflow_name] = Workflow(rules=comparison_rules, fallback=f)

    out = {"A": [], "R": []}
    for line in raw_part_ratings.splitlines():
        rating = eval("dict" + line.replace("{", "(").replace("}", ")"))
        current_workflow = "in"
        while current_workflow not in ("A", "R"):
            workflow = workflows[current_workflow]
            current_workflow = workflow(rating)
        out[current_workflow].append(rating)

    print(sum(
        sum(r.values())
        for r in out["A"]
    ))


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input.txt"))
