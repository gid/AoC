"""https://adventofcode.com/2022/day/8"""
import math
import os

from itertools import product


with open(os.path.join(os.path.dirname(__file__), f"inputs/day08_input.txt")) as f:
    actual_input = f.read()


sample_input = """30373
25512
65332
33549
35390"""


def solve(inputs: str) -> None:
    yx = tuple(tuple(map(int, l)) for l in inputs.splitlines())
    xy = tuple(tuple(l) for l in zip(*yx))
    w, visible, scores = len(xy), 0, set()
    for x, y in product(range(w), range(w)):
        views = (yx[y][0:x][::-1], yx[y][x + 1 : w], xy[x][0:y][::-1], xy[x][y + 1 : w])
        visible += int(any(all(tree < xy[x][y] for tree in view) for view in views))
        scores.add(
            math.prod(
                next((i for i, h in enumerate(view, 1) if h >= yx[y][x]), len(view))
                for view in views
            )
        )
    print(f"Part 1: {visible}")
    print(f"Part 2: {max(scores)}\n")


solve(sample_input)
solve(actual_input)
