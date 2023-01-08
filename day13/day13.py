# Advent of Code: Day 13
__author__ = "Matteo Golin"

# Imports
import json
import functools
from enum import Enum

# Constants
PacketPair = tuple[list, list]
PacketPairList = list[PacketPair]


class ComparisonState(Enum):

    """Defines the Troolean state of comparisons."""
    FALSE = 0
    TRUE = 1
    EQUAL = 2


# Helper functions
def parse_pairs(raw_pairs: list[str]) -> PacketPairList:

    """Returns the raw input packets as a list of pairs, parsed into Python lists and ints."""

    pair_list: PacketPairList = []
    for pair in raw_pairs:

        # Process into Python objects
        first, second = pair.split("\n")
        first = json.loads(first)
        second = json.loads(second)

        pair_list.append((first, second))

    return pair_list


def in_order(item1: int | list, item2: int | list) -> ComparisonState:

    """Returns true if the items are in the right order, otherwise returns false."""

    type1 = type(item1)
    type2 = type(item2)

    # Both ints
    if type1 is int and type2 is int:

        if item1 < item2:  # Smaller number needs to be on left for correct order
            return ComparisonState.TRUE
        elif item1 > item2:
            return ComparisonState.FALSE
        else:
            return ComparisonState.EQUAL

    # Both lists
    elif type1 is list and type2 is list:

        # Go through each list item one by one
        # Those comparisons can return true or false early
        # If none of them do and the left runs out of items first, return True
        # If none of them do and the right runs out of items first, return False
        # Otherwise, this pair is equal

        # Iterate through lists
        length = max(len(item1), len(item2))
        for _ in range(length):

            try:
                left = item1[_]
                right = item2[_]
                result = in_order(left, right)

                # Order has been determined
                if result != ComparisonState.EQUAL:
                    return result

            # A list ran out of items
            except IndexError:
                if len(item1) == length:  # Left was the longest
                    return ComparisonState.FALSE
                return ComparisonState.TRUE  # Right was the longest

        return ComparisonState.EQUAL

    # One int one list
    else:

        # Convert integer item to a list containing that integer and re-compare
        if type1 is int:
            return in_order([item1], item2)
        else:
            return in_order(item1, [item2])


def bubble_sort(packets: list) -> None:

    """Puts packets in order."""

    n = len(packets)

    for i in range(n):
        for j in range(0, n - i - 1):
            if not in_order(packets[j], packets[j + 1]) == ComparisonState.TRUE:
                packets[j], packets[j + 1] = packets[j + 1], packets[j]


# Main
def main():

    # Load input
    with open("input.txt", 'r') as file:
        raw_pairs: list[str] = file.read().split("\n\n")
    pairs: PacketPairList = parse_pairs(raw_pairs)

    # Part 1
    # What is the sum of the indices of the packet pairs that are in order, starting indexing at 1
    ordered: list[int] = []

    for _ in range(len(pairs)):

        item1, item2 = pairs[_]
        result = in_order(item1, item2)

        if result == ComparisonState.TRUE:
            ordered.append(_ + 1)

    print(f"The sum of the indices in the correct order is {sum(ordered)}.")

    # Part 2
    # Put all the packets in order including divider packets, then return the product of the divider packet indices
    DIVIDER1 = [[2]]
    DIVIDER2 = [[6]]

    # Destructure pairs
    all_pairs = [DIVIDER1, DIVIDER2]
    for pair in pairs:
        all_pairs.extend(list(pair))

    bubble_sort(all_pairs)

    decoder_key = (all_pairs.index(DIVIDER1) + 1) * (all_pairs.index(DIVIDER2) + 1)
    print(f"The decoder key for the distress signal is {decoder_key}.")


if __name__ == "__main__":
    main()
