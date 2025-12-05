"""https://adventofcode.com/2025/day/5"""

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 5)


example_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


def collapse_ranges(ranges: list[list[int]]) -> list[list[int]]:
    collapsed_ranges = []
    for low, high in ranges:
        for collapsed_low_high in collapsed_ranges:
            if not (high < collapsed_low_high[0] or low > collapsed_low_high[1]):
                collapsed_low_high[0] = min(collapsed_low_high[0], low)
                collapsed_low_high[1] = max(collapsed_low_high[1], high)
                break
        else:
            collapsed_ranges.append([low, high])
    return collapsed_ranges


def solve(inputs: str):
    fresh_range_list, ingredients_list = inputs.split("\n\n")

    fresh_ranges = [
        (int(a), int(b))
        for a, b in (line.split("-") for line in fresh_range_list.splitlines())
    ]

    fresh_count = 0
    for ingredient in list(map(int, ingredients_list.splitlines())):
        for fresh_range in fresh_ranges:
            if fresh_range[0] <= ingredient <= fresh_range[1]:
                fresh_count += 1
                break
    print(f"Part 1: {fresh_count}")

    while True:
        prior_range_len = len(fresh_ranges)
        fresh_ranges = collapse_ranges(fresh_ranges)
        if len(fresh_ranges) == prior_range_len:
            break
    print(f"Part 2: {sum(b - a + 1 for a, b in fresh_ranges)}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
