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


def collapse_ranges(ranges):
    collapsed = []
    for fresh_range in ranges:
        for existing_range in collapsed:
            # check if fresh_range overlaps existing_range
            if not (
                fresh_range[1] < existing_range[0] or fresh_range[0] > existing_range[1]
            ):
                existing_range[0] = min(existing_range[0], fresh_range[0])
                existing_range[1] = max(existing_range[1], fresh_range[1])
                break
        else:
            collapsed.append([fresh_range[0], fresh_range[1]])
    return collapsed


def solve(inputs: str):
    fresh_range_list, ingredients_list = inputs.split("\n\n")
    ingredient_ids = list(map(int, ingredients_list.splitlines()))

    fresh_ranges = []
    for a, b in (line.split("-") for line in fresh_range_list.splitlines()):
        fresh_ranges.append([int(a), int(b)])

    fresh_count = 0
    for ingredient in ingredient_ids:
        for fresh_range in fresh_ranges:
            if fresh_range[0] <= ingredient <= fresh_range[1]:
                fresh_count += 1
                break
    print(f"Part 1: {fresh_count}")

    range_count = len(fresh_ranges)
    while True:
        fresh_ranges = collapse_ranges(fresh_ranges)
        if len(fresh_ranges) == range_count:
            break
        range_count = len(fresh_ranges)

    total_fresh = 0
    for fresh_range in fresh_ranges:
        total_fresh += fresh_range[1] - fresh_range[0] + 1

    print(f"Part 2: {total_fresh}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
