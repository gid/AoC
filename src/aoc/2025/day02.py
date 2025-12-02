"""https://adventofcode.com/2025/day/2"""

import re

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 2)


example_input = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""


pattern = re.compile(r"^(.+)\1+$")


def solve(inputs: str):
    ranges = inputs.split(",")

    part1, part2 = 0, 0
    for start_end in ranges:
        start, end = map(int, start_end.split("-"))
        for number in range(start, end + 1):
            str_num = str(number)
            if not pattern.fullmatch(str_num):
                continue

            part2 += number
            q, r = divmod(len(str_num), 2)
            if r == 0 and str_num[:q] == str_num[q:]:
                part1 += number

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}\n")


solve(example_input)
solve(actual_input)
