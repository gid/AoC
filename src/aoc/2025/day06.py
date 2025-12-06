"""https://adventofcode.com/2025/day/6"""

import math

from collections import defaultdict

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 6)


example_input = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """


def solve(inputs: str):
    lines = inputs.splitlines()
    number_lines, operator_line = lines[:-1], lines[-1]
    assert len(set(len(line) for line in number_lines)) == 1

    operators = operator_line.split()
    numbers = [[] for _ in range(len(operators))]

    for line in number_lines:
        for i, value in enumerate(line.split()):
            numbers[i].append(int(value))
    answers = [math.prod(vals) if op == "*" else sum(vals) for vals, op in zip(numbers, operators)]
    print(f"Part 1: {sum(answers)}")

    grand_total = 0

    right_chars = "".join(s[-1] for s in number_lines)
    while operators:
        while right_chars.isspace():
            number_lines = [s[:-1] for s in number_lines]
            right_chars = "".join(s[-1] for s in number_lines)

        values = []
        while not right_chars.isspace():
            values.append(int(right_chars))
            number_lines = [s[:-1] for s in number_lines]
            if not number_lines[0]:
                break
            right_chars = "".join(s[-1] for s in number_lines)

        operators, operator = operators[:-1], operators[-1]
        grand_total += math.prod(values) if operator == "*" else sum(values)

    print(f"Part 2: {grand_total}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
