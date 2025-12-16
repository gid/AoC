"""https://adventofcode.com/2025/day/10"""

from collections import deque
from z3 import Optimize, Int, sat, Sum

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 10)


example_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


def fewest_indicator_presses(target: int, toggles: list[int]) -> int:

    initial_state = 0
    queue = deque([(initial_state, 0)])
    visited = {initial_state}
    while queue:
        current_state, presses = queue.popleft()
        if current_state == target:
            return presses
        for toggle in toggles:
            next_state = current_state ^ toggle
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, presses + 1))

    raise ValueError


def solve_z3(button_matrix: list[list[int]], target: list[int]) -> int:
    n_buttons = len(button_matrix[0])

    s = Optimize()

    button_presses = [Int(f"b{i}") for i in range(n_buttons)]
    for bp in button_presses:
        s.add(bp >= 0)

    for row, rhs in zip(button_matrix, target):
        expr = Sum(row[j] * button_presses[j] for j in range(n_buttons))
        s.add(expr == rhs)

    s.minimize(Sum(button_presses))

    if s.check() == sat:
        model = s.model()
        return sum(model.evaluate(bp).as_long() for bp in button_presses)
    else:
        print(button_matrix, target)
        raise ValueError("No solution found")


def solve(inputs: str):

    indicator_presses = []
    joltage_presses = []

    machine_specs = inputs.splitlines()
    for machine_spec in machine_specs:
        indicators_spec, *wiring_specs, joltage_spec = machine_spec.split(" ")

        indictors_spec = indicators_spec.strip("[]").replace("#", "1").replace(".", "0")
        indicators_target = int(indictors_spec[::-1], 2)
        joltages = list(map(int, joltage_spec.strip("{}").split(",")))
        button_matrix = [[0 for _ in range(len(wiring_specs))] for _ in range(len(joltages))]
        indicator_toggles = []
        for button_i, wiring_spec in enumerate(wiring_specs):
            toggles = list(map(int, wiring_spec.strip("()").split(",")))
            indicator_toggles.append(sum(2**i for i in toggles))
            for joltage_i in toggles:
                button_matrix[joltage_i][button_i] = 1

        indicator_presses.append(fewest_indicator_presses(indicators_target, indicator_toggles))
        joltage_presses.append(solve_z3(button_matrix, joltages))

    print(f"Part 1: {sum(indicator_presses)}")
    print(f"Part 2: {sum(joltage_presses)}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
