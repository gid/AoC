"""https://adventofcode.com/2025/day/10"""

from collections import deque

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 10)


example_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


def fewest_presses(indicators_target: int, indicator_toggles: list[int]) -> int:

    initial_state = 0
    queue = deque([(initial_state, 0)])
    visited = {initial_state}
    while queue:
        current_state, presses = queue.popleft()
        if current_state == indicators_target:
            return presses
        for toggle in indicator_toggles:
            next_state = current_state ^ toggle
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, presses + 1))

    raise ValueError


def solve(inputs: str):

    machines = []
    machine_specs = inputs.splitlines()
    for machine_spec in machine_specs:
        indicators_spec, *wiring_specs, joltage_spec = machine_spec.split(" ")

        indictors_spec = indicators_spec.strip("[]").replace("#", "1").replace(".", "0")
        indicators_target = int(indictors_spec[::-1], 2)

        indicator_toggles = []
        for wiring_spec in wiring_specs:
            button_toggles = wiring_spec.strip("()").split(",")
            indicator_toggles.append(sum(2**i for i in map(int, button_toggles)))
        machines.append((indicators_target, indicator_toggles))

    print(f"Part 1: {sum(fewest_presses(*machine) for machine in machines)}")
    print(f"Part 2: {False}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
