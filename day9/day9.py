# Advent of Code: Day 9
__author__ = "Matteo Golin"

# Imports

# Constants
INPUT_FILE = "./input.txt"
Coordinates = tuple[int, int]
Region = list[list[str]]

# Movement directions
MOVEMENTS: dict[str, Coordinates] = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1)
}

# Surrounding 8 cell vectors
SURROUNDING: dict[str, Coordinates] = {
    "left": (-1, 0),
    "right": (1, 0),
    "top-left": (-1, -1),
    "bottom-left": (-1, 1),
    "bottom-right": (1, 1),
    "top-right": (1, -1),
    "up": (0, -1),
    "down": (0, 1),
    "on": (0, 0),
}

# Maps head locations to how tail should move
HEAD_SPOTS: dict[Coordinates, str] = {
    (0, -2): "up",
    (0, 2): "down",
    (-2, 0): "left",
    (2, 0): "right",
    (-2, -1): "top-left",
    (-1, -2): "top-left",
    (-2, -2): "top-left",
    (1, -2): "top-right",
    (2, -1): "top-right",
    (2, -2): "top-right",
    (-2, 1): "bottom-left",
    (-1, 2): "bottom-left",
    (-2, 2): "bottom-left",
    (2, 1): "bottom-right",
    (1, 2): "bottom-right",
    (2, 2): "bottom-right",
}


# Main
def add_points(start: Coordinates, translation: Coordinates) -> Coordinates:

    """Returns the sum of two points."""

    return start[0] + translation[0], start[1] + translation[1]


def subtract_points(first: Coordinates, second: Coordinates) -> Coordinates:

    """Returns the difference between two coordinates."""

    return first[0] - second[0], first[1] - second[1]


def print_region(region: Region) -> None:

    """Prints the region."""

    for row in region:
        for column in row:
            print(column, end="")
        print()


def calculate_tail(head: Coordinates, tail: Coordinates) -> Coordinates:

    """Returns the new tail position."""

    # If the tail is touching the head in any capacity, it does not move
    difference = subtract_points(head, tail)
    for cell in SURROUNDING.values():
        if difference == cell:
            return tail

    # Calculate move
    move = HEAD_SPOTS[difference]
    move = SURROUNDING[move]

    return add_points(tail, move)


def main():

    # Read input
    moves = []
    with open(INPUT_FILE, 'r') as file:
        for line in file:
            direction, amount = line.strip().split(" ")
            moves.append((direction, int(amount)))

    # Create bridge environment
    region: Region = [["." for _ in range(6)] for _ in range(5)]
    start: Coordinates = (0, 4)
    region[4][0] = "s"

    # Part 1
    # How many positions does the tail touch at least once
    head: Coordinates = start  # Head and tail begin at the start
    tail: Coordinates = start

    # Simulate movement
    tail_positions = {start}
    for move in moves:

        # Unpacking data
        direction, amount = move
        direction = MOVEMENTS[direction]

        # Move head and then calculate how the tail moves in response
        for _ in range(amount):

            head = add_points(head, direction)

            tail = calculate_tail(head, tail)

            # Record tail
            tail_positions.add(tail)

    print(f"The tail visited {len(tail_positions)} places at least once.")

    # Part 2
    # How many positions does the tail of rope length 10 touch at least once
    length: int = 10
    rope: list[Coordinates] = [start for _ in range(length)]
    tail_positions = {start}
    for move in moves:

        # Unpacking data
        direction, amount = move
        direction = MOVEMENTS[direction]

        # Move head and then calculate how the tail moves in response
        for _ in range(amount):

            # Update head
            rope[0] = add_points(rope[0], direction)

            # Calculate movement for each segment behind the head
            for _ in range(1, len(rope[1:]) + 1):
                rope[_] = calculate_tail(rope[_ - 1], rope[_])

            # Record positions
            tail_positions.add(rope[-1])

    print(f"The tail of length {length} visited {len(tail_positions)} places at least once.")


if __name__ == '__main__':
    main()
