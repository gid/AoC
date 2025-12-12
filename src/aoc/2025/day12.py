"""https://adventofcode.com/2025/day/12"""

from collections import defaultdict
from dataclasses import dataclass, field

from aoc_utils import get_input_data, print_time_taken

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


class Xy(complex):
    @property
    def x(self) -> int:
        return int(self.real)

    @property
    def y(self) -> int:
        return int(self.imag)

    def __init__(self, x, y):
        super().__init__(x, y)


TILE_PLACEMENT_OFFSETS = [Xy(x, y) for x in range(-2, 3) for y in range(-2, 3) if (x, y) != (0, 0)]
TILE_PLACEMENT_OFFSETS.sort(key=lambda p: (p[0] ** 2 + p[1] ** 2, p[0], p[1]))


class Tile:

    def __init__(self, tile_id: int, pattern_data: list[str]):
        assert len(pattern_data) == 3 and all(len(row) == 3 for row in pattern_data)
        self.tile_id = tile_id
        pattern = set()
        for y, row in enumerate(pattern_data, start=-1):
            for x, ch in enumerate(row, start=-1):
                if ch == "#":
                    pattern.add(Xy(x, y))
        self.transforms = set()
        for _ in range(2):
            for _ in range(4):
                pattern = {-1j * p for p in pattern}  # Rotate 90° clockwise
                self.transforms.add(pattern)
            pattern = {-p.real + 1j * p.imag for p in pattern}  # Flip horizontal


@dataclass(slots=True)
class Region:

    max_width: int
    max_height: int
    target: tuple[int, int, int, int, int, int]
    border_xy: set[tuple[Xy]] = field(default_factory=set)
    filled_xy: set[tuple[Xy]] = field(default_factory=set)
    tiles_used: list[int] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0])

    @property
    def current_width(self) -> int:
        if not self.filled_xy:
            return 0
        return max((p.x for p in self.filled_xy)) - min((p.x for p in self.filled_xy)) + 1

    @property
    def current_height(self) -> int:
        if not self.filled_xy:
            return 0
        return max((p.y for p in self.filled_xy)) - min((p.y for p in self.filled_xy)) + 1

    def places_to_add_tile(self, tile: Tile) -> set[Xy]:
        """Possible places to add tile to border of region."""
        if not self.filled_xy:
            return {Xy(0, 0)}

        possible_places = set()
        for region_xy in self.filled_xy:
            for delta in TILE_PLACEMENT_OFFSETS:
                for xy in tile.pattern:
                    if any(region_xy + delta + xy in self.filled_xy for xy in tile.pattern):
                        break
                else:
                    possible_places.add(region_xy + delta)
        return possible_places

    def add_tile(self, tile: Tile, xy: Xy) -> None:
        """Adds a tile at position xy and updates border."""
        for tile_xy in tile.pattern:
            self.filled_xy.add(xy + tile_xy)
        self.tiles_used[tile.tile_id] += 1


def solve(inputs: str):
    *all_tile_data, all_region_data = inputs.strip().split("\n\n")

    regions: list[Region] = []
    for region_data in all_region_data.splitlines():
        w_x_h, tile_usage = region_data.split(": ")
        width, height = map(int, w_x_h.split("x"))
        target = tuple(map(int, tile_usage.split(" ")))
        regions.append(Region(width, height, target))

    tiles: list[Tile] = []
    for tile_data in all_tile_data.split("\n\n"):
        id_line, *pattern_data = tile_data.splitlines()
        tile_id = int(id_line.rstrip(":"))
        tiles.append(Tile(tile_id, pattern_data))

    for region in regions:
        for place_xy in region.places_to_add_tile(tile):
            if (
                region.current_width + tile.width <= region.max_width
                and region.current_height + tile.height <= region.max_height
            ):
                region.add_tile(tile, place_xy)

    values = tuple(map(int, inputs.splitlines()))

    print(f"Part 1: {False}")
    print(f"Part 2: {False}\n")


if __name__ == "__main__":
    solve(example_input)
    # solve(actual_input)
