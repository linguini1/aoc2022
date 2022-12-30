# Advent of Code: Day 3
__author__ = "Matteo Golin"

# Imports
from string import ascii_lowercase, ascii_uppercase

# Constants
INPUT_FILE = "./input.txt"
PRIORITIES = list(ascii_lowercase + ascii_uppercase)


# Main
def common_item_type(items: str) -> str:

    """Returns the common item type within the two compartments of the rucksack."""

    # Split items into two compartments
    first_comp = items[:len(items) // 2]
    second_comp = items[len(items) // 2:]

    # Find common item type
    first_comp = set(first_comp)
    second_comp = set(second_comp)

    return list(first_comp.intersection(second_comp))[0]


def group_intersection(group: list[str]) -> str:

    """Returns the common item type between three rucksacks in a group."""

    group = [set(rucksack) for rucksack in group]
    common = group[0]

    for rucksack in group[1:]:
        common = common.intersection(rucksack)

    return list(common)[0]


def main():

    # Part 1
    # What is the sum of the priorities of the item types in common between compartments in the rucksack
    priorities = []
    with open(INPUT_FILE, 'r') as file:

        for line in file:
            line = line.strip()
            common = common_item_type(line)
            priorities.append(PRIORITIES.index(common) + 1)

    print(f"The sum of the priorities is {sum(priorities)}")

    # Part 2
    # What is the sum of the priorities of the item types that each elf of three in a group have in common
    counter: int = 0
    priorities = []
    current_group: list[str] = []
    with open(INPUT_FILE, 'r') as file:

        for line in file:
            counter += 1  # Increment counter
            current_group.append(line.strip())

            # Beginning of new group
            if counter % 3 == 0:
                common = group_intersection(current_group)
                priorities.append(PRIORITIES.index(common) + 1)

                current_group = []

    print(f"The sum of the badge priorities is {sum(priorities)}")


if __name__ == '__main__':
    main()