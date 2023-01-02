# Advent of Code: Day 10
__author__ = "Matteo Golin"

# Imports

# Constants
INPUT_FILE = "./input.txt"
RECORDED_CYCLES: list[int] = [20, 60, 100, 140, 180, 220]
Screen = list[list[str]]


# Main
def crt_display(sprite_pos: int, cycle: int, screen: Screen) -> None:

    """Updates the CRT screen with the pixels being drawn each cycle."""

    x = cycle % 40
    y = cycle // 40

    # Skip if nothing is drawn
    if x not in [sprite_pos - 1, sprite_pos, sprite_pos + 1]:
        return

    # Draw pixel
    screen[y][x] = "▓"


def show_screen(screen: Screen) -> None:

    """Prints the screen."""

    for row in screen:
        for pixel in row:
            print(pixel, end="")
        print()


def main():

    # Read input
    with open(INPUT_FILE, 'r') as file:
        operations: list[str] = file.read().split("\n")[:-1]  # Empty final line
    operations2 = operations.copy()

    # Part 1
    # What is the sum of the six key signal strengths

    # Start operations
    x_register = 1
    program_counter = 1
    waiting = 0
    signal_strengths = []

    while operations or waiting:

        # Catch the important cycles
        if program_counter in RECORDED_CYCLES:
            signal_strengths.append(program_counter * x_register)

        if not waiting:
            operation = operations.pop(0)  # Operation marked as complete

        # Increment X register
        if "addx" in operation:
            if waiting == 1:
                waiting = 0
                x_register += int(operation.split(" ")[1])
            else:
                waiting += 1

        program_counter += 1

    print(f"The sum of the 6 key signal strengths is {sum(signal_strengths)}.")

    # Part 2
    # What 8 capital letters appear on the CRT screen

    # Create screen
    screen: Screen = [[" " for _ in range(40)] for _ in range(6)]

    # Perform operations
    x_register = 1
    waiting = 0
    program_counter = 0
    while operations2 or waiting:

        crt_display(x_register, program_counter, screen)

        if not waiting:
            operation = operations2.pop(0)  # Operation marked as complete

        # Increment X register
        if "addx" in operation:
            if waiting == 1:
                waiting = 0
                x_register += int(operation.split(" ")[1])
            else:
                waiting += 1

        program_counter += 1

    print("\nThe CRT screen output is:\n")
    show_screen(screen)


if __name__ == '__main__':
    main()
