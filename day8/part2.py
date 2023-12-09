from __future__ import annotations

import re
from collections import defaultdict
from functools import reduce
from itertools import cycle
from math import gcd
from typing import Dict

from utils import getInput, timeit


# singleton to access nodes in the tree via name
NODES: Dict[str, Node] = {}


class Node:
    def __init__(self, label: str, left: str, right: str):
        self.label = label

        self.children = {"L": left, "R": right}

        self.start = label.endswith("A")
        self.end = label.endswith("Z")

    def __getitem__(self, direction: str) -> Node:
        return NODES[self.children[direction]]

    def __repr__(self):
        return f"Node({self.label})"


node_ptrn = re.compile(r'(?P<label>\w+)\s=\s\((?P<left>\w+),\s(?P<right>\w+)\)')


def lcm(numbers):
    return reduce(
        (lambda x, y: int(x * y / gcd(x, y)))
        , numbers
    )


@timeit
def main(aoc: str):
    lines = aoc.splitlines()

    directions = cycle(lines[0].strip())
    for line in lines[2:]:
        m = node_ptrn.match(line)
        label, left, right = m.group("label"), m.group("left"), m.group("right")
        NODES[label] = Node(label, left, right)

    current_nodes = [n for n in NODES.values() if n.start]
    n_nodes = len(current_nodes)

    # Try to figure out the idx of the start/stops of the cycles
    ends = defaultdict(list)

    for idx, d in enumerate(directions):
        # stop only when you have enough data to calc lcm
        if len(ends) == n_nodes and min([len(v) for v in ends.values()]) == 2:
            break

        next_nodes = []

        for jdx, n in enumerate(current_nodes):
            next_node = n[d]
            next_nodes.append(next_node)
            if next_node.end:
                ends[jdx].append(idx+1)

        current_nodes = next_nodes

    out = lcm([
        v[-1] - v[-2]
        for v in ends.values()
    ])

    print(out)


if __name__ == "__main__":
    main(getInput("./input-test-3.txt"))
    main(getInput("./input.txt"))
