"""https://adventofcode.com/2025/day/8"""

import heapq
import math
from itertools import combinations
from typing import NamedTuple

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


class JunctionBox(NamedTuple):
    x: int
    y: int
    z: int

    def distance_to(self, other: "JunctionBox") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5


def solve(inputs: str, part_1_connections: int) -> None:
    box_circuit = {JunctionBox(*map(int, line.split(","))): i for i, line in enumerate(inputs.splitlines())}
    circuits = {i: {box} for box, i in box_circuit.items()}
    distances = [(a.distance_to(b), a, b) for a, b in combinations(box_circuit.keys(), 2)]
    heapq.heapify(distances)

    connections_made = 0
    while len(circuits) > 1:
        _, a, b = heapq.heappop(distances)
        a_circuit, b_circuit = box_circuit[a], box_circuit[b]
        if a_circuit != b_circuit:
            for box in circuits[b_circuit]:
                box_circuit[box] = a_circuit
            circuits[a_circuit].update(circuits[b_circuit])
            circuits.pop(b_circuit)

        connections_made += 1
        if connections_made == part_1_connections:
            print(f"Part 1: {math.prod(heapq.nlargest(3, (len(s) for s in circuits.values())))}")

    print(f"Part 2: {a.x * b.x}\n")


if __name__ == "__main__":
    solve(example_input, 10)
    solve(actual_input, 1000)
