"""https://adventofcode.com/2025/day/10"""

from collections import deque

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 10)


example_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]


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


def fewest_joltage_presses(target: tuple[int], toggles: list[tuple[int]]) -> int:

    initial_state = (0,) * len(target)
    queue = deque([(initial_state, 0)])
    visited = {initial_state}
    while queue:
        current_state, presses = queue.popleft()
        if current_state == target:
            return presses
        for toggle in toggles:
            next_states = list(current_state)
            for i in toggle:
                next_states[i] += 1
            next_state = tuple(next_states)
            if any(next_state[i] > target[i] for i in range(len(target))):
                continue
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, presses + 1))

    raise ValueError


def solve(inputs: str):

    machine_indicators = []
    machine_joltages = []

    machine_specs = inputs.splitlines()
    for machine_spec in machine_specs:
        indicators_spec, *wiring_specs, joltage_spec = machine_spec.split(" ")

        indictors_spec = indicators_spec.strip("[]").replace("#", "1").replace(".", "0")
        indicators_target = int(indictors_spec[::-1], 2)

        joltages = joltage_spec.strip("{}").split(",")
        joltage_target = tuple(map(int, joltages))

        indicator_toggles, joltage_toggles = [], []
        for wiring_spec in wiring_specs:
            toggles = list(map(int, wiring_spec.strip("()").split(",")))
            indicator_toggles.append(sum(2**i for i in toggles))
            joltage_toggles.append(toggles)

        machine_indicators.append((indicators_target, indicator_toggles))
        machine_joltages.append((joltage_target, joltage_toggles))

    print(f"Part 1: {sum(fewest_indicator_presses(target, toggles) for target, toggles in machine_indicators)}")
    print(f"Part 2: {sum(fewest_joltage_presses(target, toggles) for target, toggles in machine_joltages)}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
