"""https://adventofcode.com/2025/day/3"""

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 3)


example_input = """987654321111111
811111111111119
234234234234278
818181911112111"""


def max_joltage(bank: str, num_batteries: int) -> int:
    if num_batteries == 1:
        return int(max(bank))

    for j in range(9, 0, -1):
        try:
            idx = bank[: -(num_batteries - 1)].index(str(j))
            return j * (10 ** (num_batteries - 1)) + max_joltage(
                bank[idx + 1 :], num_batteries - 1
            )
        except ValueError:
            continue


def solve(inputs: str):
    banks = inputs.splitlines()
    print(f"Part 1: {sum(max_joltage(bank, num_batteries=2) for bank in banks)}")
    print(f"Part 2: {sum(max_joltage(bank, num_batteries=12) for bank in banks)}\n")


solve(example_input)
solve(actual_input)
