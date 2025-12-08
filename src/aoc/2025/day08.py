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
    junction_box_circuit = {JunctionBox(*map(int, line.split(","))): i for i, line in enumerate(inputs.splitlines())}
    circuits = {i: {junction_box} for junction_box, i in junction_box_circuit.items()}

    distances = []
    for a, b in combinations(junction_box_circuit.keys(), 2):
        heapq.heappush(distances, (a.distance_to(b), a, b))

    n_connections = 0
    while len(circuits) > 1:
        _, a, b = heapq.heappop(distances)
        if junction_box_circuit[a] != junction_box_circuit[b]:
            a_circuit, b_circuit = junction_box_circuit[a], junction_box_circuit[b]
            for junction_box in circuits[b_circuit]:
                junction_box_circuit[junction_box] = a_circuit
            circuits[a_circuit].update(circuits[b_circuit])
            circuits.pop(b_circuit)
        n_connections += 1
        if n_connections == part_1_connections:
            print(f"Part 1: {math.prod(heapq.nlargest(3, (len(s) for s in circuits.values())))}")

    print(f"Part 2: {a.x * b.x}\n")


if __name__ == "__main__":
    solve(example_input, 10)
    solve(actual_input, 1000)
