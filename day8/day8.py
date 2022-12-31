# Advent of Code: Day 8
__author__ = "Matteo Golin"

# Imports
import math

# Constants
INPUT_FILE = "./input.txt"
Coordinates = tuple[int, int]


# Main
def main():

    # Unpack input
    with open(INPUT_FILE, 'r') as file:
        raw_data = file.read().split("\n")[:-1]  # Ignore blank final line

    # 2D array representation
    forest = []
    for row in raw_data:
        forest.append([int(tree) for tree in row])

    # Part 1
    # How many trees are visible from outside the grid
    # Loop through forest excluding edges
    visible = 0
    outer_trees = len(forest[0]) * 2 + len(forest) * 2 - 4
    for y in range(1, len(forest) - 1):
        for x in range(1, len(forest[0]) - 1):

            tree = forest[y][x]
            row = forest[y]
            column = [forest[_][x] for _ in range(len(forest))]

            # Visible from left or right
            if max(row[:x]) < tree or max(row[x + 1:]) < tree:
                visible += 1

            # Visible from top or bottom
            elif max(column[:y]) < tree or max(column[y + 1:]) < tree:
                visible += 1

    print(f"The number of trees visible from the outside of the grid is {visible + outer_trees}.")

    # Part 2
    # What is the highest scenic score possible for any tree in the forest
    best_tree: tuple[Coordinates, int] = ((0, 0), 0)
    for y in range(1, len(forest) - 1):
        for x in range(1, len(forest[0]) - 1):

            scores = [0] * 4  # Record scores

            tree = forest[y][x]
            row = forest[y]
            column = [forest[_][x] for _ in range(len(forest))]

            directions = [
                column[y + 1:],  # Look down
                list(reversed(row[:x])),  # Look left
                list(reversed(column[:y])),  # Look up
                row[x + 1:],  # Look right
            ]

            for i in range(len(directions)):
                for other_tree in directions[i]:
                    scores[i] += 1
                    if other_tree >= tree:
                        break

            score = math.prod(scores)
            if score > best_tree[1]:
                best_tree = ((x, y), score)

    print(f"The highest possible scenic score is {best_tree[1]}.")


if __name__ == '__main__':
    main()
