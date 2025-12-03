"""https://adventofcode.com/2025/day/3"""

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 3)


example_input = """987654321111111
811111111111119
234234234234278
818181911112111"""


def max_joltage(bank: str, batteries: int) -> int:

    if batteries == 1:
        return int(max(bank))

    batteries -= 1
    max_battery = int(max(bank[:-batteries]))
    bank = bank[bank.index(str(max_battery)) + 1 :]
    return max_battery * (10**batteries) + max_joltage(bank, batteries)


def solve(inputs: str):
    banks = inputs.splitlines()
    print(f"Part 1: {sum(max_joltage(bank, batteries=2) for bank in banks)}")
    print(f"Part 2: {sum(max_joltage(bank, batteries=12) for bank in banks)}\n")


solve(example_input)
solve(actual_input)
