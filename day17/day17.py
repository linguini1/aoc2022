# Advent of Code: Day 17
__author__ = "Matteo Golin"

from typing import Literal, TypeAlias, Iterable, Optional

# All rocks relative to bottom leftmost edge
Coordinate: TypeAlias = tuple[int, int]
JetStream: TypeAlias = list[Literal[1, -1]]

HORIZONTAL: tuple[Coordinate, Coordinate, Coordinate, Coordinate] = ((0, 0), (1, 0), (2, 0), (3, 0))
PLUS: tuple[Coordinate, Coordinate, Coordinate, Coordinate, Coordinate] = ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1))
L: tuple[Coordinate, Coordinate, Coordinate, Coordinate, Coordinate] = ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))
VERTICAL: tuple[Coordinate, Coordinate, Coordinate, Coordinate] = ((0, 0), (0, 1), (0, 2), (0, 3))
CUBE: tuple[Coordinate, Coordinate, Coordinate, Coordinate] = ((0, 0), (0, 1), (1, 0), (1, 1))
ROCKS: list[tuple[Coordinate, ...]] = [HORIZONTAL, PLUS, L, VERTICAL, CUBE]

CHAMBER_WIDTH: int = 7
LFT_OFF: int = 2
BTM_OFF: int = 3
ROCKS_TO_FALL: int = 2022


dropped_rocks = []


def translate_coord(coord: Coordinate, offset: Coordinate) -> Coordinate:
    return (coord[0] + offset[0], coord[1] + offset[1])


def translate(rock: Iterable[Coordinate], offset: Coordinate) -> tuple[Coordinate, ...]:
    return tuple(translate_coord(c, offset) for c in rock)


def drop_rock(cur_rock: int, cur_jet: int, topology: list[int], jet_stream: JetStream) -> int:
    """Does one dropped rock cycle and returns the current jet."""

    rock = translate(ROCKS[cur_rock], (LFT_OFF, max(topology) + BTM_OFF))  # 2 from left, 3 above highest rock
    while True:
        # Push rock first
        push = jet_stream[cur_jet]
        translated_rock = translate(rock, (push, 0))
        if all(0 <= x < CHAMBER_WIDTH and y >= topology[x] for x, y in translated_rock):
            rock = translated_rock

        # Translate rock downward
        translated_rock = translate(rock, (0, -1))
        if not all(y >= topology[x] for x, y in translated_rock):
            for x, y in rock:
                topology[x] = max(topology[x], y + 1)
            dropped_rocks.append(rock)
            return (cur_jet + 1) % len(jet_stream)
        rock = translated_rock

        cur_jet = (cur_jet + 1) % len(jet_stream)


def print_image(topology: list[int], cur_rock: Optional[tuple[Coordinate, ...]] = None) -> None:
    height = max(topology) + BTM_OFF
    if cur_rock is not None:
        height += max(cur_rock, key=lambda x: x[1])[1] - max(topology)

    image = [["." for _ in range(CHAMBER_WIDTH)] for _ in range(height)]
    for rock in dropped_rocks:
        for c in rock:
            image[(height - 1) - c[1]][c[0]] = "#"

    # Add current rock
    if cur_rock is not None:
        for c in cur_rock:
            image[(height - 1) - c[1]][c[0]] = "@"

    # Print
    for row in image:
        for char in row:
            print(char, end="")
        print()


# Main
if __name__ == "__main__":
    # Parse input
    jet_stream: JetStream = []
    with open("./example.txt") as file:
        jet_stream = list(map(lambda x: 1 if x == ">" else -1, file.read().strip()))

    # Part 1: How tall is the tower after 2022 rocks have fallen?
    cur_rock = 0
    cur_jet = 0
    total_rocks = 0
    topology = [0 for _ in range(CHAMBER_WIDTH)]

    while total_rocks < ROCKS_TO_FALL:
        cur_jet = drop_rock(cur_rock, cur_jet, topology, jet_stream)
        cur_rock = (cur_rock + 1) % len(ROCKS)
        total_rocks += 1

    print(f"The tower of rocks will be {max(topology)} units tall after {ROCKS_TO_FALL} rocks have stopped falling.")
