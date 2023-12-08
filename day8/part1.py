from __future__ import annotations

import re
from itertools import cycle
from typing import Dict

from utils import getInput, timeit


# singleton to access nodes in the tree via name
NODES: Dict[str, Node] = {}


class Node:
    def __init__(self, label: str, left: str, right: str):
        self.label = label

        self.children = {
            "L": left,
            "R": right
        }

    def __getitem__(self, direction: str) -> Node:
        return NODES[self.children[direction]]

    def __repr__(self):
        return f"Node({self.label})"


node_ptrn = re.compile(r'(?P<label>\w+)\s=\s\((?P<left>\w+),\s(?P<right>\w+)\)')


@timeit
def main(aoc: str):
    lines = aoc.splitlines()

    directions = cycle(lines[0].strip())
    for line in lines[2:]:
        m = node_ptrn.match(line)
        label, left, right = m.group("label"), m.group("left"), m.group("right")
        NODES[label] = Node(label, left, right)

    node = NODES["AAA"]
    for idx, d in enumerate(directions):
        node = node[d]

        if node.label == "ZZZ":
            print(idx + 1)
            break


if __name__ == "__main__":
    main(getInput("./input-test.txt"))
    main(getInput("./input-test-2.txt"))
    main(getInput("./input.txt"))
