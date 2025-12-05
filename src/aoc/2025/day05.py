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
    for start, end in ranges:
        for collapsed_range in collapsed_ranges:
            if not (end < collapsed_range[0] or start > collapsed_range[1]):
                collapsed_range[0] = min(collapsed_range[0], start)
                collapsed_range[1] = max(collapsed_range[1], end)
                break
        else:
            collapsed_ranges.append([start, end])
    return collapsed_ranges


def solve(inputs: str):
    fresh_range_list, ingredients_list = inputs.split("\n\n")

    fresh_ranges = [(int(a), int(b)) for a, b in (line.split("-") for line in fresh_range_list.splitlines())]

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
    print(f"Part 2: {sum(end - start + 1 for start, end in fresh_ranges)}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
