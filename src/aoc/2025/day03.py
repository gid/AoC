"""https://adventofcode.com/2025/day/3"""

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 3)


example_input = """987654321111111
811111111111119
234234234234278
818181911112111"""


def find_biggest_joltage(bank: str, battery_count: int) -> int:
    if battery_count == 1:
        return int(max(bank))

    for j in range(9, 0, -1):
        try:
            idx = bank[: -(battery_count - 1)].index(str(j))
        except ValueError:
            continue
        return j * (10 ** (battery_count - 1)) + find_biggest_joltage(
            bank[idx + 1 :], battery_count - 1
        )
    raise ValueError("No valid joltage found")


def solve(inputs: str):
    banks = inputs.splitlines()

    total_joltage = 0
    for bank in banks:
        total_joltage += find_biggest_joltage(bank, 2)
    print(f"Part 1: {total_joltage}")

    total_joltage = 0
    for bank in banks:
        joltage = find_biggest_joltage(bank, 12)
        total_joltage += joltage
    print(f"Part 2: {total_joltage}\n")


solve(example_input)
solve(actual_input)
