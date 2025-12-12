"""https://adventofcode.com/2025/day/12"""

from collections.abc import Iterator
from heapq import heappop, heappush

from aoc_utils import get_input_data

actual_input = get_input_data(2025, 12)


example_input = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""


TILE_PLACEMENT_OFFSETS = [complex(x, y) for x in range(-2, 3) for y in range(-2, 3) if (x, y) != (0, 0)]
TILE_PLACEMENT_OFFSETS.sort(key=lambda p: (p.real**2 + p.imag**2, p.real, p.imag))


def workable_region(
    max_width: int, max_height: int, target: tuple[int, ...], shapes: dict[int, set[frozenset]], shape_sizes: dict[int, int]
) -> bool:
    """Checks if a region can fit all the shapes"""
    if sum(shape_sizes[shape_id] * usage for shape_id, usage in enumerate(target)) > max_width * max_height:
        return False  # Will never fit

    if max_width // 3 * max_height // 3 >= sum(target):
        return True  # Plenty of space to fit everything

    raise NotImplementedError("This problem is NP-Hard in general - no efficient solution known")

    # Code below was nice... but ultimately only worked on small stopping cases (failed on example 3)

    def blob_width(blob: frozenset[complex]) -> int:
        x_coords = [int(p.real) for p in blob]
        return max(x_coords, default=-1) - min(x_coords, default=0) + 1

    def blob_height(blob: frozenset[complex]) -> int:
        y_coords = [int(p.imag) for p in blob]
        return max(y_coords, default=-1) - min(y_coords, default=0) + 1

    def possible_next_steps(
        blob: frozenset[complex], shapes_needed: set[int]
    ) -> Iterator[tuple[complex, int, frozenset[complex]]]:
        placement_xys = set(blob_xy + offset for blob_xy in blob for offset in TILE_PLACEMENT_OFFSETS)
        for shape_id, shape_patterns in shapes.items():
            if shape_id not in shapes_needed:
                continue
            for shape_pattern in shape_patterns:
                if not placement_xys:
                    yield (complex(0, 0), shape_id, shape_pattern)
                for placement_xy in placement_xys:
                    if not any((placement_xy + p) in blob for p in shape_pattern):
                        yield (placement_xy, shape_id, shape_pattern)

    to_visit: list[tuple[int, int, frozenset[complex], tuple[int, ...]]] = []
    initial_blob, initial_area = frozenset(), 0
    heappush(to_visit, (sum(target), initial_area, initial_blob, target))
    visited: set[frozenset[complex]] = set((initial_blob, target))

    while to_visit:
        _, _, current_blob, current_target = heappop(to_visit)
        shapes_needed = {i for i, usage in enumerate(current_target) if usage > 0}
        if not shapes_needed:
            return True
        next_steps = list(possible_next_steps(current_blob, shapes_needed))
        for placement_xy, shape_id, shape_pattern in next_steps:
            next_blob = frozenset(current_blob | {placement_xy + p for p in shape_pattern})
            width, height = blob_width(next_blob), blob_height(next_blob)

            if width > max_width or height > max_height:
                continue
            next_target = tuple(t - 1 if i == shape_id else t for i, t in enumerate(current_target))
            if (next_blob, next_target) in visited:
                continue
            visited.add((next_blob, next_target))
            heappush(to_visit, (sum(next_target), width * height, next_blob, next_target))

    return False


def solve(inputs: str):
    *all_shape_data, all_region_data = inputs.strip().split("\n\n")

    regions = []
    for region_data in all_region_data.splitlines():
        w_x_h, shape_usage = region_data.split(": ")
        width, height = map(int, w_x_h.split("x"))
        target = tuple(map(int, shape_usage.split(" ")))
        regions.append((width, height, target))

    shapes: dict[int, set[frozenset]] = {}
    shape_sizes: dict[int, int] = {}
    for shape_data in all_shape_data:
        id_line, *pattern_data = shape_data.splitlines()
        shape_id = int(id_line.rstrip(":"))
        pattern: set[complex] = set()
        for y, row in enumerate(pattern_data, start=-1):
            for x, ch in enumerate(row, start=-1):
                if ch == "#":
                    pattern.add(complex(x, y))
        shape_sizes[shape_id] = len(pattern)
        shapes[shape_id] = set()
        for _ in range(2):
            for _ in range(4):
                pattern = frozenset(-1j * p for p in pattern)  # Rotate 90° clockwise
                shapes[shape_id].add(pattern)
            pattern = frozenset(-p.real + 1j * p.imag for p in pattern)  # Flip horizontal

    workable_regions = 0
    for i, (width, height, target) in enumerate(regions):
        if workable_region(width, height, target, shapes, shape_sizes):
            workable_regions += 1

    print(f"Part 1: {workable_regions}\n")


if __name__ == "__main__":
    # solve(example_input) NP-Hard on third example!
    solve(actual_input)
