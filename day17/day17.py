# Advent of Code: Day 17
__author__ = "Matteo Golin"

from typing import Literal, TypeAlias, Iterable, Optional

# All rocks relative to bottom leftmost edge
Coordinate: TypeAlias = tuple[int, int]
Rock: TypeAlias = set[Coordinate]
JetStream: TypeAlias = list[Literal[1, -1]]

HORIZONTAL: Rock = {(0, 0), (1, 0), (2, 0), (3, 0)}
PLUS: Rock = {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)}
L: Rock = {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}
VERTICAL: Rock = {(0, 0), (0, 1), (0, 2), (0, 3)}
CUBE: Rock = {(0, 0), (0, 1), (1, 0), (1, 1)}
ROCKS: list[Rock] = [HORIZONTAL, PLUS, L, VERTICAL, CUBE]

CHAMBER_WIDTH: int = 7
LFT_OFF: int = 2
BTM_OFF: int = 3
ROCKS_TO_FALL: int = 2022


def translate_coord(coord: Coordinate, offset: Coordinate) -> Coordinate:
    """Returns the translated coordinate."""
    return (coord[0] + offset[0], coord[1] + offset[1])


def translate(rock: Iterable[Coordinate], offset: Coordinate) -> Rock:
    """Returns the translated rock."""
    return set(translate_coord(c, offset) for c in rock)


def height(occupied: set[Coordinate]) -> int:
    """Returns the height of the rock tower so far."""
    return max(occupied, key=lambda x: x[1])[1]


def drop_rock(cur_rock: int, cur_jet: int, jet_stream: JetStream, occupied: set[Coordinate]) -> int:
    """Does one dropped rock cycle and returns the current jet."""

    # Translate rock away from side and highest rock to start
    rock = translate(ROCKS[cur_rock], (LFT_OFF, height(occupied) + BTM_OFF + 1))
    while True:
        # Push rock first
        push = jet_stream[cur_jet]
        translated_rock = translate(rock, (push, 0))

        # Only push rock if it does not hit another rock and does not exceed walls
        if not occupied & translated_rock and all(0 <= x < CHAMBER_WIDTH for x, _ in translated_rock):
            rock = translated_rock

        # Translate rock downward
        translated_rock = translate(rock, (0, -1))
        if occupied & translated_rock:  # If the rock will intersect with another...
            occupied.update(rock)  # Record rock spaces as occupied
            return (cur_jet + 1) % len(jet_stream)  # Return next jet
        rock = translated_rock

        cur_jet = (cur_jet + 1) % len(jet_stream)


def print_image(occupied: set[Coordinate], cur_rock: Optional[Rock] = None) -> None:
    """Prints the rock stack in the same format as Advent of Code's example."""
    h = height(occupied) + BTM_OFF
    if cur_rock is not None:
        h += max(cur_rock, key=lambda x: x[1])[1] - (h - BTM_OFF)

    image = [["." for _ in range(CHAMBER_WIDTH)] for _ in range(h)]
    for x, y in occupied:
        image[(h - 1) - y][x] = "#"

    # Add current rock
    if cur_rock is not None:
        for x, y in cur_rock:
            image[(h - 1) - y][x] = "@"

    # Print
    for row in image:
        for char in row:
            print(char, end="")
        print()


# Main
if __name__ == "__main__":
    # Parse input
    jet_stream: JetStream = []
    with open("./input.txt") as file:
        jet_stream = list(map(lambda x: 1 if x == ">" else -1, file.read().strip()))

    # Part 1: How tall is the tower after 2022 rocks have fallen?
    cur_rock = 0
    cur_jet = 0
    total_rocks = 0
    occupied: set[Coordinate] = set((_, 0) for _ in range(CHAMBER_WIDTH))

    while total_rocks < ROCKS_TO_FALL:
        cur_jet = drop_rock(cur_rock, cur_jet, jet_stream, occupied)
        cur_rock = (cur_rock + 1) % len(ROCKS)
        total_rocks += 1

    print(f"The tower of rocks will be {height(occupied)} units tall after {ROCKS_TO_FALL} rocks have stopped falling.")
