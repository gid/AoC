"""https://adventofcode.com/2025/day/8"""

import heapq
import math

from itertools import combinations

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 8)


example_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


def solve(inputs: str, part_1_connections: int) -> None:
    junction_box_circuit = {}
    for i, line in enumerate(inputs.splitlines()):
        junction_box_circuit[tuple(map(int, line.split(",")))] = i

    circuits = {i: {junction_box} for junction_box, i in junction_box_circuit.items()}

    distances = []
    for a, b in combinations(junction_box_circuit.keys(), 2):
        distance = (
            abs(a[0] - b[0]) ** 2 + abs(a[1] - b[1]) ** 2 + abs(a[2] - b[2]) ** 2
        ) ** 0.5
        heapq.heappush(distances, (distance, min(a, b), max(a, b)))

    n_connections = 0
    while len(circuits) > 1:
        _, a, b = heapq.heappop(distances)
        if junction_box_circuit[b] != junction_box_circuit[a]:
            a_circuit, b_circuit = junction_box_circuit[a], junction_box_circuit[b]
            for junction_box in circuits[b_circuit]:
                junction_box_circuit[junction_box] = a_circuit
            circuits[a_circuit].update(circuits[b_circuit])
            circuits.pop(b_circuit)
        n_connections += 1
        if n_connections == part_1_connections:
            top3_sizes = heapq.nlargest(3, (len(s) for s in circuits.values()))
            print(f"Part 1: {math.prod(top3_sizes)}")

    print(f"Part 2: {a[0] * b[0]}\n")


if __name__ == "__main__":
    solve(example_input, 10)
    solve(actual_input, 1000)
