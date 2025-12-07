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
    max_y = y + 1

    timelines = defaultdict(int, {start_x: 1})
    beams = {start_x}
    splits = 0
    for y in range(max_y):
        new_beams = set()
        for x in beams:
            if (x, y) in splitters:
                splits += 1
                new_beams |= {x - 1, x + 1}
                timelines[x - 1] += timelines[x]
                timelines[x + 1] += timelines[x]
                timelines[x] = 0
            else:
                new_beams.add(x)
        beams = new_beams

    print(f"Part 1: {splits}")
    print(f"Part 2: {sum(timelines.values())}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
