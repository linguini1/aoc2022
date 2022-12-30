# Advent of Code: Day 4
__author__ = "Matteo Golin"

# Imports

# Constants
INPUT_FILE = "./input.txt"
Range = tuple[int, int]
Pair = tuple[Range, Range]


def create_pair(line: str) -> Pair:

    """Returns a pair of ranges from the file line."""

    pair = line.split(",")
    r1, r2 = pair[0].split("-")
    r3, r4 = pair[1].split("-")

    return (int(r1), int(r2)), (int(r3), int(r4))


def fully_overlapping(range1: Range, range2: Range) -> bool:

    """Returns True if one of the ranges fully contains the other."""

    minimum = min(range1[0], range2[0])
    maximum = max(range1[1], range2[1])

    return (minimum, maximum) in [range1, range2]


def overlapping(range1: Range, range2: Range) -> bool:

    """Returns True if the ranges are overlapping in any capacity."""

    if range1[1] < range2[0] or range2[1] < range1[0]:
        return False

    return True


# Main
def main():

    # Unpack input
    pairs = []
    with open(INPUT_FILE, 'r') as file:
        for line in file:
            pairs.append(create_pair(line))

    # Part 1
    # In how many assignment pairs does one range fully contain the other
    overlap_count = 0
    for pair in pairs:
        if fully_overlapping(*pair):
            overlap_count += 1

    print(f"The number of fully overlapping pairs is {overlap_count}.")

    # Part 2
    # How many assignment pairs have ranges that overlap at all
    overlap_count = 0
    for pair in pairs:
        if overlapping(*pair):
            overlap_count += 1

    print(f"The number of overlapping pairs is {overlap_count}.")


if __name__ == '__main__':
    main()
