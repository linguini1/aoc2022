# Advent of Code: Day 1
__author__ = "Matteo Golin"

# Constants
INPUT_FILE = "./input.txt"


# Main
def part_1(calorie_totals: list[int]) -> None:

    """Code for Part 1"""

    # Determine the maximum sum
    maximum: int = max(calorie_totals)
    print(f"The elf carrying the most calories is carrying: {maximum} calories")


def part_2(calorie_totals: list[int]) -> None:

    """Code for Part 2"""

    top_3: list[int] = sorted(calorie_totals, reverse=True)[0:3]
    maximum: int = sum(top_3)

    print(f"The sum of the top three elves' calories is {maximum} calories.")


def main():

    # Read in input
    with open(INPUT_FILE, 'r') as file:
        raw_input = file.read()

    # Each elf is separated by a new line
    elf_list: list[str] = raw_input.split("\n\n")

    # Split individual calorie counts
    elf_calories: list[list[str]] = []
    for elf in elf_list:
        elf_calories.append(elf.split("\n"))
    elf_calories[-1].pop(-1)  # Last item will be empty string because of how split works

    # Convert calories to integers and sum them
    calorie_totals: list[int] = []
    for elf in elf_calories:
        elf = [int(calorie) for calorie in elf]
        calorie_totals.append(sum(elf))

    # Part 1
    # How many total calories is carried by the elf carrying the most calories?
    part_1(calorie_totals)

    # Part 2
    # How many calories total are the top three elves carrying
    part_2(calorie_totals)


if __name__ == '__main__':
    main()
