"""https://adventofcode.com/2025/day/1"""

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 1)


example_input = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""


def solve(inputs: str):
    rotations = inputs.splitlines()

    value = 50
    hit_zero, clicked_on_zero = 0, 0

    for rotation in rotations:
        turn, amount = rotation[0], int(rotation[1:])

        if amount == 0:
            continue

        clicked_on_zero += amount // 100
        amount = amount % 100

        original_value = value
        if turn == "L":
            value -= amount
        else:
            value += amount

        if value % 100 == 0:
            hit_zero += 1
            if amount > 0:
                clicked_on_zero += 1
        else:
            if value // 100 != 0:
                clicked_on_zero += int(original_value != 0)

        value = value % 100

        # print(f"Turn: {turn}{amount}    Value: {value%100}    Hit0: {hit_zero}   Pass0: {clicked_on_zero}")

    print(f"Part 1: {hit_zero}")
    print(f"Part 2: {clicked_on_zero}\n")


solve(example_input)
solve(actual_input)
