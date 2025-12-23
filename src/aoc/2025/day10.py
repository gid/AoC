"""https://adventofcode.com/2025/day/10
Based on the ideas discussed here:
https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
"""

from collections import defaultdict
from functools import cache
from itertools import combinations
from math import inf


from aoc_utils import get_input_data

actual_input = get_input_data(2025, 10)


example_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


def minimum_presses(machine_spec: str) -> tuple[int, int]:

    indicators_spec, *wiring_schematics, joltage_spec = machine_spec.split(" ")

    target_parity = tuple(map(int, indicators_spec[1:-1].replace("#", "1").replace(".", "0")))
    joltage_target = tuple(map(int, joltage_spec[1:-1].split(",")))

    buttons = []
    for wiring_schematic in wiring_schematics:
        toggles = list(map(int, wiring_schematic[1:-1].split(",")))
        buttons.append(tuple(int(i in toggles) for i in range(len(joltage_target))))

    # Get all possible combinations of single button presses and store the joltage changes and costs for each target parity
    button_combos = [tuple(combo) for r in range(1, len(buttons) + 1) for combo in combinations(buttons, r)]
    parity_combos = defaultdict(list)
    for button_combo in button_combos:
        joltage_change = tuple(map(sum, zip(*button_combo)))
        indicator_parity = tuple(i % 2 for i in joltage_change)
        cost_of_joltage_change = len(button_combo)
        parity_combos[indicator_parity].append((joltage_change, cost_of_joltage_change))

    # Make sure to add an option for doing nothing (0 cost, 0 joltage change)
    zero_change = tuple(0 for _ in joltage_target)
    parity_combos[zero_change].append((zero_change, 0))

    # Part 1 answer is the lowest combination of button presses that achieves the target indicator parity
    part1 = min(cost for _, cost in parity_combos[target_parity])

    @cache
    def _minimum_presses(joltage_target: tuple[int, ...]) -> int:
        if all(j == 0 for j in joltage_target):
            return 0

        target_parity = tuple(j % 2 for j in joltage_target)
        retval = inf
        for joltage_changes, cost in parity_combos[target_parity]:
            new_joltage_target = [target - delta for target, delta in zip(joltage_target, joltage_changes)]
            if any(j < 0 for j in new_joltage_target):
                continue
            new_joltage_target = tuple(j // 2 for j in new_joltage_target)
            retval = min(retval, cost + 2 * _minimum_presses(new_joltage_target))

        return retval

    part2 = _minimum_presses(joltage_target)

    return (part1, part2)


def solve(inputs: str):
    machine_specs = inputs.splitlines()
    answers = [minimum_presses(machine_spec) for machine_spec in machine_specs]
    print(f"Part 1: {sum(answer[0] for answer in answers)}")
    print(f"Part 2: {sum(answer[1] for answer in answers)}\n")


if __name__ == "__main__":
    solve(example_input)
    solve(actual_input)
