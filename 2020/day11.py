import os
from collections import defaultdict

from grid import XY

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
with open(os.path.join(script_dir, f"inputs/{script_name}_input.txt")) as f:
    actual_input = f.read()

sample_input = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


class ChairSystem:
    FLOOR = "."
    EMPTY = "L"
    OCCUPIED = "#"

    def __init__(self, inputs, tolerance, immediate_neighbours_only=True):
        self.tolerance = tolerance

        self.chairs = set()
        self.occupied = set()

        x, y = 0, 0
        for y, line in enumerate(inputs.split()):
            for x, c in enumerate(line):
                if c != self.FLOOR:
                    chair = XY(x, y)
                    self.chairs.add(chair)
                    if c == self.OCCUPIED:
                        self.occupied.add(chair)
        max_x, max_y = x, y

        self.in_sight = defaultdict(set)
        for chair in self.chairs:
            for direction in XY.all_directions():
                xy = chair
                while True:
                    xy += direction
                    if not xy.in_bounds(max_x, max_y):
                        break
                    if xy in self.chairs:
                        self.in_sight[chair].add(xy)
                        break
                    if immediate_neighbours_only:
                        break

    def iterate(self):
        new_occupied = set()
        for chair in self.chairs:
            occupied_count = sum(c in self.occupied for c in self.in_sight[chair])
            if chair not in self.occupied:
                if occupied_count == 0:
                    new_occupied.add(chair)
            else:
                if occupied_count < self.tolerance:
                    new_occupied.add(chair)
        self.occupied = new_occupied

    def find_stable_state(self):
        while True:
            prior_state = frozenset(self.occupied)
            self.iterate()
            if frozenset(self.occupied) == prior_state:
                return len(self.occupied)


def solve(inputs):
    chairs = ChairSystem(inputs, tolerance=4)
    print(f"Part 1: {chairs.find_stable_state()}")
    chairs = ChairSystem(inputs, tolerance=5, immediate_neighbours_only=False)
    print(f"Part 2: {chairs.find_stable_state()}\n")


solve(sample_input)
solve(actual_input)