"""https://adventofcode.com/2025/day/7"""

from collections import defaultdict

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 7)


example_input = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""


def solve(inputs: str):
    splitters = set()
    for y, row in enumerate(inputs.splitlines()):
        for x, c in enumerate(row):
            if y == 0 and c == "S":
                start_x = x
            if c == "^":
                splitters.add((x, y))
    max_x, max_y = x + 1, y + 1

    beams, splits = {start_x}, 0
    for y in range(max_y):
        new_beams = set()
        for x in beams:
            if (x, y) in splitters:
                new_beams |= {x - 1, x + 1}
                splits += 1
            else:
                new_beams.add(x)
        beams = new_beams
    print(f"Part 1: {splits}")

    timelines = defaultdict(int)
    timelines[start_x] = 1
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in splitters:
                timelines[x - 1] += timelines[x]
                timelines[x + 1] += timelines[x]
                timelines[x] = 0

    print(f"Part 2: {sum(timelines.values())}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
