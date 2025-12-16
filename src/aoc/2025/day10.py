"""https://adventofcode.com/2025/day/10"""

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

    target_polarity = tuple(map(int, indicators_spec[1:-1].replace("#", "1").replace(".", "0")))
    joltage_target = tuple(map(int, joltage_spec[1:-1].split(",")))

    n_counters = len(joltage_target)

    toggles = []
    for wiring_schematic in wiring_schematics:
        button_ids = list(map(int, wiring_schematic[1:-1].split(",")))
        toggles.append(tuple(int(i in button_ids) for i in range(n_counters)))

    # Get all possible combinations of single button presses and store the resulting indicator polarity and joltage changes
    button_combos = [tuple(combo) for r in range(1, len(toggles) + 1) for combo in combinations(toggles, r)]
    combo_sums = {}
    polarity_combos = defaultdict(list)
    for combo in button_combos:
        combo_sums[combo] = tuple(map(sum, zip(*combo)))
        indicator_polarity = tuple(i % 2 for i in combo_sums[combo])
        polarity_combos[indicator_polarity].append(combo)

    # Part 1 answer is the shortest combination of button presses that achieves the target indicator polarity
    part1 = len(min(polarity_combos[target_polarity], key=len))

    @cache
    def _minimum_presses(joltage_target: tuple[int, ...]) -> int:
        if all(j == 0 for j in joltage_target):
            return 0

        target_polarity = tuple(j % 2 for j in joltage_target)
        retval = inf
        for combo in polarity_combos[target_polarity]:
            new_joltage_target = [target - combo_sum for target, combo_sum in zip(joltage_target, combo_sums[combo])]
            if any(j < 0 for j in new_joltage_target):
                continue
            assert all(j % 2 == 0 for j in new_joltage_target)
            new_joltage_target = tuple(j // 2 for j in new_joltage_target)
            retval = min(retval, len(combo) + 2 * _minimum_presses(new_joltage_target))

        return retval

    part2 = _minimum_presses(joltage_target)

    return (part1, part2)


def solve(inputs: str):
    machine_specs = inputs.splitlines()
    answers = [minimum_presses(machine_spec) for machine_spec in machine_specs[-1:]]
    print(f"Part 1: {sum(answer[0] for answer in answers)}")
    print(f"Part 2: {sum(answer[1] for answer in answers)}\n")


if __name__ == "__main__":
    solve(example_input)
    # solve(actual_input)
