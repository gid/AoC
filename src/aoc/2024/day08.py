"""https://adventofcode.com/2024/day/8"""

from collections import defaultdict
from itertools import combinations

from aoc_utils import get_input_data

actual_input = get_input_data(2024, 8)


example_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


def solve(inputs: str):
    antennas = defaultdict(list)
    for y, row in enumerate(inputs.splitlines()):
        for x, c in enumerate(row):
            xy = complex(x, y)
            if c != ".":
                antennas[c].append(xy)
    height, width = y + 1, x + 1

    antinodes_part1, antinodes_part2 = set(), set()
    for antenna_positions in antennas.values():
        for a, b in combinations(antenna_positions, 2):
            for antenna_xy, dxy in ((a, a - b), (b, b - a)):
                multiplier, in_grid = 0, True
                while in_grid:
                    antinode = antenna_xy + (dxy * multiplier)
                    in_grid = 0 <= antinode.real < width and 0 <= antinode.imag < height
                    if in_grid:
                        antinodes_part2.add(antinode)
                        if multiplier == 1:
                            antinodes_part1.add(antinode)
                    multiplier += 1

    print(f"Part 1: {len(antinodes_part1)}")
    print(f"Part 2: {len(antinodes_part2)}\n")


solve(example_input)
solve(actual_input)
