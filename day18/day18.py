# Advent of Code: Day 18
__author__ = "Matteo Golin"

from typing import Self
from dataclasses import dataclass

NEIGHBOURS: list[tuple[int, int, int]] = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
]


@dataclass
class Coordinate:
    """Represents a coordinate in 3D space."""

    x: int
    y: int
    z: int

    def __add__(self, other: Self) -> Self:
        if type(other) != Coordinate:
            raise TypeError(f"Addition between {self.__class__.__name__} and {type(other)} is not supported.")
        return Coordinate(self.x + other.x, self.y + other.y, self.z + other.z)

    def neighbours(self) -> set[Self]:
        """Returns a set of the coordinate's neighbours."""
        return set(self.__class__(self.x + x, self.y + y, self.z + z) for x, y, z in NEIGHBOURS)

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    __repr__ = __str__


def parse_input(file_path: str) -> set[Coordinate]:
    """Parses the puzzle input into 3D coordinates."""
    coordinates = set()
    with open(file_path, "r") as file:
        for line in file:
            coordinates.add(Coordinate(*list(map(int, line.split(",")))))
    return coordinates


def graphify(coords: set[Coordinate]) -> dict[Coordinate, set[Coordinate]]:
    """Return a graph showing connections between one cube and the others."""
    graph = dict()
    for coord in coords:
        graph[coord] = coords & coord.neighbours()
    return graph


def surface_area(coords: set[Coordinate]) -> int:
    """Returns the surface area of the object described by the coordinates."""
    sa = 0
    for connections in graphify(coords).values():
        sa += 6 - len(connections)
    return sa


# Main
def main():
    print("Part 1: What is the surface area of the lava droplet")
    print(f"TEST: {surface_area(parse_input('test.txt'))}")
    print(surface_area(parse_input("input.txt")))


if __name__ == "__main__":
    main()
