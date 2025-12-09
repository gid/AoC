"""https://adventofcode.com/2025/day/9"""

import heapq

from itertools import combinations

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 9)


example_input = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


NORTH, SOUTH, EAST, WEST = (0, -1), (0, 1), (1, 0), (-1, 0)


def direction(a, b):
    if a[0] == b[0]:
        return SOUTH if a[1] < b[1] else NORTH
    elif a[1] == b[1]:
        return EAST if a[0] < b[0] else WEST
    raise ValueError("Not aligned")


def solve(inputs: str):
    tiles = [
        (int(a), int(b)) for a, b in (line.split(",") for line in inputs.splitlines())
    ]

    largest_areas = []
    for a, b in combinations(tiles, 2):
        width = abs(a[0] - b[0]) + 1
        height = abs(a[1] - b[1]) + 1
        area = width * height
        heapq.heappush(largest_areas, (-area, a, b))

    print(f"Part 1: {largest_areas[0][0] * -1}")

    # Four options for corners
    # top_right = set()  # ┐
    # bottom_left = set()  # └
    # bottom_right = set()  # ┘
    # top_left = set()  # ┌
    # full_loop = [tiles[-1]] + tiles + [tiles[0]]
    # for prior_xy, xy, next_xy in zip(full_loop[:-2], full_loop[1:-1], full_loop[2:]):
    #     turn = (direction(prior_xy, xy), direction(xy, next_xy))
    #     if turn == (NORTH, EAST) or turn == (WEST, SOUTH):
    #         top_left.add(xy)
    #     if turn == (NORTH, WEST) or turn == (EAST, SOUTH):
    #         top_right.add(xy)
    #     if turn == (SOUTH, EAST) or turn == (WEST, NORTH):
    #         bottom_left.add(xy)
    #     if turn == (SOUTH, WEST) or turn == (EAST, NORTH):
    #         bottom_right.add(xy)
    #     if abs(xy[0] - prior_xy[0]) == 1 or abs(xy[1] - prior_xy[1]) == 1:
    #         raise ValueError("Double back!")

    full_loop = tiles + [tiles[0]]
    horizontal_edges, vertical_edges = set(), set()
    for a, b in zip(full_loop[:-1], full_loop[1:]):
        if a[0] == b[0]:
            vertical_edges.add((a[0], (min(a[1], b[1]), max(a[1], b[1]))))
        elif a[1] == b[1]:
            horizontal_edges.add(((min(a[0], b[0]), max(a[0], b[0])), a[1]))
        if abs(a[0] - b[0]) == 1 or abs(a[1] - b[1]) == 1:
            raise ValueError("Double back!")

    while True:
        area, a_xy, b_xy = heapq.heappop(largest_areas)

        min_x, max_x = min(a_xy[0], b_xy[0]), max(a_xy[0], b_xy[0])
        min_y, max_y = min(a_xy[1], b_xy[1]), max(a_xy[1], b_xy[1])
        if min_x == max_x or min_y == max_y:
            break
        good_area = True
        # Check horizontal and vertical borders and confirm no intersecting edges
        for x in range(min_x + 1, max_x):
            if any(
                edge_x == x and edge_min_y < min_y < edge_max_y
                for edge_x, (edge_min_y, edge_max_y) in vertical_edges
            ):
                good_area = False
            if any(
                edge_x == x and edge_min_y < max_y < edge_max_y
                for edge_x, (edge_min_y, edge_max_y) in vertical_edges
            ):
                good_area = False
        for x in (min_x, max_x):
            if not all(
                edge_max_y < min_y
                or edge_min_y > max_y
                or (edge_min_y == min_y and edge_max_y == max_y)
                for edge_x, (edge_min_y, edge_max_y) in vertical_edges
                if edge_x == x
            ):
                good_area = False
        for y in range(min_y + 1, max_y):
            if any(
                edge_y == y and edge_min_x < min_x < edge_max_x
                for (edge_min_x, edge_max_x), edge_y in horizontal_edges
            ):
                good_area = False
            if any(
                edge_y == y and edge_min_x < max_x < edge_max_x
                for (edge_min_x, edge_max_x), edge_y in horizontal_edges
            ):
                good_area = False
        for y in (min_y, max_y):
            if not all(
                edge_max_x < min_x
                or edge_min_x > max_x
                or (edge_min_x == min_x and edge_max_x == max_x)
                for (edge_min_x, edge_max_x), edge_y in horizontal_edges
                if edge_y == y
            ):
                good_area = False

        # # Start top left walking east and avoiding top rights
        # if any((x, min_y) in top_right for x in range(min_x, max_x)):
        #     good_area = False
        # # Walk south avoiding bottom rights
        # if any((max_x, y) in bottom_right for y in range(min_y, max_y)):
        #     good_area = False
        # # Walk west avoiding bottom lefts
        # if any((x, max_y) in bottom_left for x in range(max_x, min_x, -1)):
        #     good_area = False
        # # Walk north avoiding top lefts
        # if any((min_x, y) in top_left for y in range(max_y, min_y, -1)):
        #     good_area = False
        if good_area:
            break

    print(f"Part 2: {area*-1}\n")


if __name__ == "__main__":
    solve(example_input)
    # solve(actual_input)
