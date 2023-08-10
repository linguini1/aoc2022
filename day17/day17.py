# Advent of Code: Day 17
__author__ = "Matteo Golin"

from typing import Literal, TypeAlias, Iterable

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
ROCKS_TO_FALL_1: int = 2022
ROCKS_TO_FALL_2: int = 1000000000000


def translate_coord(coord: Coordinate, offset: Coordinate) -> Coordinate:
    """Returns the translated coordinate."""
    return (coord[0] + offset[0], coord[1] + offset[1])


def translate(rock: Iterable[Coordinate], offset: Coordinate) -> Rock:
    """Returns the translated rock."""
    return set(translate_coord(c, offset) for c in rock)


def height(occupied: set[Coordinate]) -> int:
    """Returns the height of the rock tower so far."""
    return max(occupied, key=lambda x: x[1])[1]


def drop_rock(
    cur_rock: int, cur_jet: int, jet_stream: JetStream, occupied: set[Coordinate], fallen: dict[str, int]
) -> int:
    """
    Does one dropped rock cycle and returns the current jet index. If a cycle is detected, then -1 is returned.
    """

    # Translate rock away from side and highest rock to start
    rock = translate(ROCKS[cur_rock % len(ROCKS)], (LFT_OFF, height(occupied) + BTM_OFF + 1))
    fall_pattern = f"{cur_rock % len(ROCKS)}"
    while True:
        # Push rock first
        push = jet_stream[cur_jet]
        translated_rock = translate(rock, (push, 0))

        # Only push rock if it does not hit another rock and does not exceed walls
        if not occupied & translated_rock and all(0 <= x < CHAMBER_WIDTH for x, _ in translated_rock):
            fall_pattern += ">" if push == 1 else "<"
            rock = translated_rock
        else:
            fall_pattern += "x"

        # Translate rock downward
        translated_rock = translate(rock, (0, -1))
        if occupied & translated_rock:  # If the rock will intersect with another...
            occupied.update(rock)  # Record rock spaces as occupied
            if fall_pattern in fallen:
                print(fall_pattern)
                fallen["cycle start"] = fallen[fall_pattern]
                return -1

            fallen[fall_pattern] = cur_rock
            return (cur_jet + 1) % len(jet_stream)  # Return next jet

        fall_pattern += "v"
        rock = translated_rock

        cur_jet = (cur_jet + 1) % len(jet_stream)


def draw_image(occupied: set[Coordinate]) -> None:
    """Prints out a visualization of the rock tower."""
    max_height = height(occupied)
    image = [["." for _ in range(CHAMBER_WIDTH)] for _ in range(max_height + BTM_OFF)]

    for x, y in occupied:
        image[y][x] = "#"

    print("-" * (CHAMBER_WIDTH + 2))
    for row in reversed(image):
        print("|", end="")
        for col in row:
            print(col, end="")
        print("|", end="")
        print()
    print("-" * (CHAMBER_WIDTH + 2))


def height_after(rocks: int) -> int:
    """Returns the height of the rock tower after the passed number of rocks have fallen."""
    cur_jet = 0
    total_rocks = 0
    occupied: set[Coordinate] = set((_, 0) for _ in range(CHAMBER_WIDTH))
    fall_patterns = dict()

    while total_rocks < rocks:
        cur_jet = drop_rock(total_rocks, cur_jet, jet_stream, occupied, fall_patterns)
        if cur_jet == -1:  # Cycle detected
            break
        total_rocks += 1

    if rocks == 5 or rocks == 20:
        draw_image(occupied)

    if cur_jet == -1:
        period_len = total_rocks - fall_patterns["cycle start"]
        print(f"Cycle detected from rock {fall_patterns['cycle start']} to rock {total_rocks}.")
        height_after(fall_patterns["cycle start"])
        height_after(total_rocks)
        print(f"Cycle has period of {period_len}")
        current_height = height(occupied)
        print(f"The current height is {current_height}")
        period_height = current_height - height_after(fall_patterns["cycle start"])
        print(f"The height of each period is {period_height}")
        periods, remainder = divmod(rocks - total_rocks, period_len)

        print(periods, remainder)
        return current_height + (periods * period_height) + height_after(remainder)

    return height(occupied)


# Main
if __name__ == "__main__":
    # Parse input
    jet_stream: JetStream = []
    with open("./example.txt") as file:
        jet_stream = list(map(lambda x: 1 if x == ">" else -1, file.read().strip()))

    # Part 1: How tall is the tower after 2022 rocks have fallen?
    h = height_after(ROCKS_TO_FALL_1)
    print(f"The tower of rocks will be {h} units tall after {ROCKS_TO_FALL_1} rocks have stopped falling.")

    # Part 2: How tall is the tower after 1000000000000 rocks have fallen.
    print(f"The tower of rocks will be {h} units tall after {ROCKS_TO_FALL_2} rocks have stopped falling.")
