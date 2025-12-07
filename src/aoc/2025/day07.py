"""https://adventofcode.com/2025/day/7"""

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

    paths = {((start_x, 0),)}
    timelines = 0
    while paths:
        path = paths.pop()
        x, y = path[-1]
        if y == max_y:
            timelines += 1
            continue
        if (x, y + 1) not in splitters:
            paths.add(path + ((x, y + 1),))
        else:
            paths |= {path + ((x + 1, y + 1),), path + ((x - 1, y + 1),)}

    print(f"Part 2: {timelines}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
