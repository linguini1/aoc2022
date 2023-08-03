# Advent of Code: Day 17
__author__ = "Matteo Golin"

from typing import Literal, TypeAlias, Iterable

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
ROCKS_TO_FALL = 10
DROPPED_ROCKS = []


def translate_coord(coord: Coordinate, offset: Coordinate) -> Coordinate:
    return (coord[0] + offset[0], coord[1] + offset[1])


def translate(rock: Iterable[Coordinate], offset: Coordinate) -> tuple[Coordinate, ...]:
    return tuple(translate_coord(c, offset) for c in rock)


def drop_rock(cur_rock: int, cur_jet: int, topology: list[int], jet_stream: JetStream) -> int:
    """Does one dropped rock cycle and returns the current jet."""

    rock = translate(ROCKS[cur_rock], (LFT_OFF, BTM_OFF + max(topology)))  # 2 from left, 3 above highest rock
    while True:
        # Check for space on the sides
        push = jet_stream[cur_jet]
        print(rock, push)
        if all(0 <= cell[0] + push < CHAMBER_WIDTH and cell[1] >= topology[cell[0] + push] for cell in rock):
            rock = translate(rock, (push, 0))

        # Check for space downward
        for cell in rock:
            translated = translate_coord(cell, (0, -1))
            if topology[translated[0]] > translated[1]:  # Rock has landed
                for c in rock:
                    topology[c[0]] = max(topology[c[0]], c[1] + 1)  # Replace with highest point
                print(rock)
                DROPPED_ROCKS.append(rock)
                print(topology)
                return (cur_jet + 1) % len(jet_stream)
        rock = translate(rock, (0, -1))

        cur_jet = (cur_jet + 1) % len(jet_stream)  # Get next jet move


# Main
if __name__ == "__main__":
    # Parse input
    jet_stream: JetStream = []
    with open("./example.txt") as file:
        jet_stream = list(map(lambda x: 1 if x == ">" else -1, file.read()))

    # Part 1: How tall is the tower after 2022 rocks have fallen?
    cur_rock = 0
    cur_jet = 0
    total_rocks = 0
    topology = [0 for _ in range(CHAMBER_WIDTH)]

    while total_rocks < ROCKS_TO_FALL:
        cur_jet = drop_rock(cur_rock, cur_jet, topology, jet_stream)
        cur_rock = (cur_rock + 1) % len(ROCKS)
        total_rocks += 1

    image = [["." for _ in range(CHAMBER_WIDTH)] for _ in range(max(topology) + BTM_OFF)]
    for rock in DROPPED_ROCKS:
        for c in rock:
            image[-c[1] - 1][c[0]] = "#"

    for row in image:
        for char in row:
            print(char, end="")
        print()

    print(f"The tower of rocks will be {max(topology)} units tall after {ROCKS_TO_FALL} rocks have stopped falling.")
