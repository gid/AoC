"""https://adventofcode.com/2025/day/9"""

import heapq
from functools import cache
from itertools import combinations
from typing import NamedTuple, Self

from aoc_utils import get_input_data, print_time_taken

actual_input = get_input_data(2025, 9)


example_input = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

EAST, SOUTH, WEST, NORTH = (1, 0), (0, 1), (-1, 0), (0, -1)
TURN_ANTICLOCKWISE = {EAST: NORTH, NORTH: WEST, WEST: SOUTH, SOUTH: EAST}
TURN_CLOCKWISE = {EAST: SOUTH, SOUTH: WEST, WEST: NORTH, NORTH: EAST}
TURN = {"L": TURN_ANTICLOCKWISE, "R": TURN_CLOCKWISE}


class Xy(NamedTuple):
    x: int
    y: int

    def heading_towards(self, other: Self) -> tuple[int, int]:
        if self.x == other.x:
            return NORTH if self.y < other.y else SOUTH
        elif self.y == other.y:
            return EAST if self.x < other.x else WEST
        else:
            raise ValueError("Points are not aligned horizontally or vertically")


# @cache
# def segments_cross(this_start: Xy, this_end: Xy, other_start: Xy, other_end: Xy) -> bool:
#     if this_start == Xy(2, 3) and this_end == Xy(7, 3) and other_start == Xy(2, 3) and other_end == Xy(9, 3):
#         pass

#     # Normalise the coordinates to make life easier
#     x0, x1 = min(this_start.x, this_end.x), max(this_start.x, this_end.x)
#     y0, y1 = min(this_start.y, this_end.y), max(this_start.y, this_end.y)
#     other_x0, other_x1 = min(other_start.x, other_end.x), max(other_start.x, other_end.x)
#     other_y0, other_y1 = min(other_start.y, other_end.y), max(other_start.y, other_end.y)

#     if (this_start.x == this_end.x) == (other_start.x == other_end.x):  # Colinear segments

#         if this_start.x == this_end.x:  # Both vertical
#             return False
#             if x0 != other_x0:
#                 return False
#             overlap = min(y1, other_y1) - max(y0, other_y0)
#             if overlap <= 0:
#                 return False
#             return not (y0 <= other_y0 < other_y1 <= y1)

#         else:  # Both horizontal
#             return False
#             if y0 != other_y0:
#                 return False
#             overlap = min(x1, other_x1) - max(x0, other_x0)
#             if overlap <= 0:
#                 return False
#             return not (x0 <= other_x0 < other_x1 <= x1)

#     # Non-colinear segments - N.B. if they share a vertex that's *not* an intersect
#     shared_vertex = {this_start, this_end} & {other_start, other_end}
#     if shared_vertex:
#         return False
#     if this_start.x == this_end.x:
#         return other_x0 <= x0 <= other_x1 and y0 <= other_y0 <= y1
#     return other_y0 <= y0 <= other_y1 and x0 <= other_x0 <= x1


# @cache
# def segment_contains_point(start: Xy, end: Xy, p: Xy) -> bool:
#     if start.x == end.x:  # vertical segment
#         if p.x != start.x:
#             return False
#         return min(start.y, end.y) <= p.y <= max(start.y, end.y)
#     else:  # horizontal segment
#         if p.y != start.y:
#             return False
#         return min(start.x, end.x) <= p.x <= max(start.x, end.x)


class Segment(NamedTuple):
    start: Xy
    end: Xy

    @property
    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    @property
    def vertices(self) -> set[Xy]:
        return {self.start, self.end}

    def intersects(self, other: Self) -> bool:
        return segments_cross(self.start, self.end, other.start, other.end)


class Polygon:
    vertices: list[Xy]

    def __init__(self, vertices: list[Xy]) -> None:
        self.vertices = vertices
        n = len(self.vertices)
        self.edges = [Segment(self.vertices[i], self.vertices[(i + 1) % n]) for i in range(n)]

        in_out = {}
        for prior_xy, this_xy, next_xy in zip([vertices[-1]] + vertices[:-1], vertices, vertices[1:] + [vertices[0]]):
            in_out[this_xy] = (prior_xy.heading_towards(this_xy), this_xy.heading_towards(next_xy))

    @cache
    def contains_point(self, p: Xy) -> bool:
        inside = False
        for edge in self.edges:

            # Can stop and return true if this segment contains the point
            if segment_contains_point(edge.start, edge.end, p):
                return True

            # Count the vertical edge intersections in the horizontal ray coming from p (ray-casting algorithm)
            if edge.is_vertical:
                if edge.start.x < p.x:
                    continue
                if min(edge.start.y, edge.end.y) < p.y <= max(edge.start.y, edge.end.y):
                    inside = not inside

        return inside

    def contains_polygon(self, other: Self) -> bool:
        if not all(self.contains_point(corner) for corner in other.vertices):
            return False
        for edge in self.edges:
            for other_edge in other.edges:
                if edge.intersects(other_edge):
                    return False
        return True


class Rectangle(Polygon):
    def __init__(self, corner1: Xy, corner2: Xy) -> None:
        super().__init__([corner1, Xy(corner2.x, corner1.y), corner2, Xy(corner1.x, corner2.y)])


@print_time_taken
def solve(inputs: str):
    tiles = [Xy(int(a), int(b)) for a, b in (line.split(",") for line in inputs.splitlines())]
    polygon = Polygon(vertices=tiles)

    largest_areas = []
    for a, b in combinations(tiles, 2):
        width = abs(a[0] - b[0]) + 1
        height = abs(a[1] - b[1]) + 1
        area = width * height
        heapq.heappush(largest_areas, (-area, a, b))

    print(f"Part 1: {largest_areas[0][0] * -1}")

    while True:
        area, corner1, corner2 = heapq.heappop(largest_areas)

        if corner1 == (9, 5) and corner2 == (2, 3):
            pass

        if polygon.contains_polygon(Rectangle(corner1, corner2)):
            break

        if -area == 1566935900:
            print("MISSED IT!")
            print(corner1, corner2)
            break

    print(f"Part 2: {area*-1}\n")


if __name__ == "__main__":
    solve(example_input)
    # solve(actual_input)
