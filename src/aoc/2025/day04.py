"""https://adventofcode.com/2025/day/4"""

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 4)


example_input = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

DIRECTIONS = [1, 1 + 1j, 1j, -1 + 1j, -1, -1 - 1j, -1j, 1 - 1j]


def count_neighbours(roll: complex, rolls: set[complex]) -> int:
    return sum(1 for d in DIRECTIONS if (roll + d) in rolls)


def accessible_rolls(rolls: set[complex]) -> set[complex]:
    return {roll for roll in rolls if count_neighbours(roll, rolls) < 4}


def solve(inputs: str):
    rolls = set()
    for y, row in enumerate(inputs.splitlines()):
        for x, c in enumerate(row):
            if c == "@":
                rolls.add(complex(x, y))

    print(f"Part 1: {len(accessible_rolls(rolls))}")
    print(f"Part 2: {False}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
