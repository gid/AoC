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
    beams = set()
    for y, row in enumerate(inputs.splitlines()):
        for x, c in enumerate(row):
            if c == "S":
                beams.add((x, y))
            if c == "^":
                splitters.add((x, y))
    max_y = y + 1
    splits = 0
    for y in range(max_y):
        new_beams = set()
        for beam in beams:
            x = beam[0]
            if (x, y) in splitters:
                new_beams.add((x - 1, y + 1))
                new_beams.add((x + 1, y + 1))
                splits += 1
            else:
                new_beams.add((x, y + 1))
        beams = new_beams

    print(f"Part 1: {splits}")
    print(f"Part 2: {False}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
