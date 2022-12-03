from __future__ import annotations
import math
import sys

from collections import deque
from functools import lru_cache
from heapq import heappush, heappop
from itertools import product
from typing import Any, Callable, Iterable, Optional


NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (0, 1)

LEFT_TURN = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}
RIGHT_TURN = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}


@lru_cache
def _direction_vectors(dimensions: int) -> tuple[tuple[int, ...], ...]:
    return tuple(product((-1, 0, 1), repeat=dimensions))


class Point(tuple):
    def __new__(cls, *args):
        return tuple.__new__(cls, args)

    def __add__(self, other):
        return type(self)(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other):
        return type(self)(*(a - b for a, b in zip(self, other)))

    @property
    def all_neighbours(self):
        """Generator for neighbouring points (including diagonal neighbours)"""
        for direction in _direction_vectors(len(self)):
            if not all(d == 0 for d in direction):
                yield self + type(self)(*direction)

    @property
    def neighbours(self):
        """Generator for immediate neighbouring points (not including diagonals)"""
        for direction in _direction_vectors(len(self)):
            if sum(abs(d) for d in direction) == 1:
                yield self + type(self)(*direction)

    @property
    def manhattan_distance(self):
        return sum(abs(d) for d in self)


class XY(Point):
    """An integer x, y coordinate/point"""

    def __new__(cls, x: int, y: int):
        return Point.__new__(cls, x, y)

    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[1]

    @classmethod
    def directions(cls):
        return [cls(*xy) for xy in product((-1, 0, 1), (-1, 0, 1)) if xy != (0, 0)]

    @classmethod
    def direction(cls, direction):
        return {
            "N": cls(0, -1),
            "S": cls(0, 1),
            "E": cls(1, 0),
            "W": cls(-1, 0),
        }[direction.upper()[0]]

    def in_bounds(self, bounds: int | tuple[int, int] | tuple[int, int, int, int]):
        min_x, min_y, max_x, max_y = 0, 0, 0, 0
        if isinstance(bounds, int):
            max_x, max_y = bounds, bounds
        elif len(bounds) == 2:
            max_x, max_y = bounds  # type: ignore
        elif len(bounds) == 4:
            min_x, min_y, max_x, max_y = bounds  # type: ignore
        return min_x <= self.x <= max_x and min_y <= self.y <= max_y


class XyGrid:
    def __init__(self, inputs: str = "", convertor: Optional[Callable] = None) -> None:
        self.grid: dict[XY, Any] = {
            XY(x, y): convertor(c) if convertor is not None else c
            for y, line in enumerate(inputs.splitlines())
            for x, c in enumerate(line)
        }

    def get_limits(self) -> tuple[int, int, int, int]:
        min_x, min_y, max_x, max_y = math.inf, math.inf, -math.inf, -math.inf
        for xy in self.grid.keys():
            min_x = min(min_x, xy.x)
            min_y = min(min_y, xy.y)
            max_x = max(max_x, xy.x + 1)
            max_y = max(max_y, xy.y + 1)
        return int(min_x), int(min_y), int(max_x), int(max_y)

    def get_symbol(self, xy: XY) -> Any:
        return self.grid.get(xy, " ")

    def print_grid(self, show_headers: bool = True) -> None:
        min_x, min_y, max_x, max_y = self.get_limits()
        header1 = "     " + "".join(
            [" " * 9 + str(x + 1) for x in range((max_x - 1) // 10)]
        )
        header2 = "    " + "".join([str(x % 10) for x in range(max_x)])
        if show_headers:
            print(header1 + "\n" + header2)
        for y in range(min_y, max_y):
            if show_headers:
                print(f"{y:3d} ", end="")
            for x in range(min_x, max_x):
                print(self.get_symbol(XY(x, y)), end="")
            if show_headers:
                print(f" {y:<3d} ", end="")
            print()
        if show_headers:
            print(header2 + "\n" + header1)

    def connected_nodes(self, node: XY, blockages: Iterable[XY] = None):
        connected_nodes = node.neighbours
        if blockages:
            connected_nodes = [n for n in connected_nodes if n not in blockages]
        return connected_nodes

    def find_shortest_path(self, start: XY, target: XY, blockages: Iterable[XY] = None):
        """Find the shortest path from start to target"""
        prior_step: dict[XY, Optional[XY]] = {start: None}
        distances: dict[XY, int] = {start: 0}
        to_visit: list[XY] = []
        heappush(to_visit, start)
        while to_visit:
            this_node = heappop(to_visit)
            if this_node == target:
                break
            distance_so_far = distances[this_node]
            for next_node in self.connected_nodes(this_node, blockages):
                if distances.get(next_node, sys.maxsize) > distance_so_far + 1:
                    distances[next_node] = distance_so_far + 1
                    heappush(to_visit, (this_node, next_node))

        return risk_level[target]