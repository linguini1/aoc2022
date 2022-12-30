# Advent of Code: Day 5
__author__ = "Matteo Golin"

# Imports

# Constants
INPUT_FILE = "./input.txt"
Movement = tuple[int, int, int]


def parse_stacks(crate_stacks: str) -> list[list[str]]:

    """Parses stacks into the actual stack representation."""

    # Remove numbering
    crate_stacks = crate_stacks.split("\n")[:-1]

    # Add comma delimiter
    stacks = []
    for line in crate_stacks:
        new_line = ""
        for _ in range(len(line)):
            if (_ + 1) % 4 != 0:
                new_line += line[_]
            else:
                new_line += ","
        stacks.append(new_line.split(","))

    # Make each stack its own list
    new_stacks = []
    for _ in range(len(stacks[0])):
        stack = []
        for i in range(len(stacks)):

            # Remove blank spaces
            crate = stacks[i][_]
            if "[" in crate:
                stack.append(crate[1])

        new_stacks.append(stack[::-1])  # Reverse stack so top is at end of list

    return new_stacks


def apply_movements(stacks: list[list[str]], movements: list[Movement]) -> None:

    """Applies the movements to the stacks."""

    for move in movements:

        # Unpack instructions
        num, origin, dest = move
        origin_stack = stacks[origin - 1]
        destination_stack = stacks[dest - 1]

        # Take # of crates from destination to origin
        for _ in range(num):
            destination_stack.append(origin_stack.pop())


def apply_movements_9001(stacks: list[list[str]], movements: list[Movement]) -> None:

    """Applies the movements to the stacks, preserving the order of crates moved in groups."""

    for move in movements:

        # Unpack instructions
        num, origin, dest = move
        origin_stack = stacks[origin - 1]
        destination_stack = stacks[dest - 1]

        # Take # of crates from destination to origin
        grouping = origin_stack[-num:]
        stacks[origin - 1] = origin_stack[:-num]
        destination_stack.extend(grouping)


# Main
def main():

    # Read in input
    with open(INPUT_FILE, 'r') as file:
        raw_data = file.read()

    # Split input into stacks and movements (split on empty line)
    crate_stacks, movements = raw_data.split("\n\n")

    # Parse stacks into lists
    crate_stacks = parse_stacks(crate_stacks)

    # Parse movements
    instructions: list[Movement] = []
    for movement in movements.split("\n")[:-1]:
        movement = movement.split(" ")
        num, origin, destination = int(movement[1]), int(movement[3]), int(movement[5])
        instructions.append((num, origin, destination))

    # Part 1
    # After the rearrangement procedure, what crate is on the top of each stack?
    crate_stacks_copy = []
    for stack in crate_stacks:
        crate_stacks_copy.append(stack.copy())

    apply_movements(crate_stacks_copy, instructions)

    print("The crates at the top of each stack are: ", end="")
    for stack in crate_stacks_copy:
        print(stack[-1], end="")
    print()

    # Part 2
    # After the rearrangement procedure (this time preserving the order of the group of crates moved at
    # once) what crate is on the top of each stack?

    apply_movements_9001(crate_stacks, instructions)

    print("The crates at the top of each stack using Crane 9001 are: ", end="")
    for stack in crate_stacks:
        print(stack[-1], end="")
    print()


if __name__ == '__main__':
    main()
