"""https://adventofcode.com/2025/day/5"""

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 5)


example_input = """xxx"""


def solve(inputs: str):
    values = tuple(map(int, inputs.splitlines()))

    print(f"Part 1: {False}")
    print(f"Part 2: {False}\n")


if __name__ == "__main__":
    solve(example_input)
    # solve(actual_input)
