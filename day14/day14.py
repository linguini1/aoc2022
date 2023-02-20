# Advent of Code: Day 14
__author__ = "Matteo Golin"

# Imports

# Constants
ROCK: str = "#"
AIR: str = "."
FALLING_SAND: str = "+"
RESTING_SAND: str = "o"
Coordinates = tuple[int, int]
Path = list[Coordinates]
Map = list[list[str]]
SAND_SOURCE: Coordinates = (500, 0)


# Helper functions
def update_bounds(x: int, y: int, bounds: dict[str, int]) -> None:
    """Updates the coordinate bounds if the current x and y coordinates past the recorded bounds."""

    if x < bounds["min_x"]:
        bounds["min_x"] = x

    if x > bounds["max_x"]:
        bounds["max_x"] = x

    if y < bounds["min_y"]:
        bounds["min_y"] = y

    if y > bounds["max_y"]:
        bounds["max_y"] = y


def path_from_line(text_path: str, bounds: dict[str, int]) -> Path:
    """Returns the list of coordinates that form a path."""

    coordinates = []
    for coord in text_path.split(" -> "):
        x, y = coord.split(",")
        x, y = int(x), int(y)

        # Look for maximum and minimum bounds
        update_bounds(x, y, bounds)

        coordinates.append((x, y))
    return coordinates


def correct_paths(paths: list[Path], xmin: int, ymin: int) -> list[Path]:
    """Normalizes the paths according to the bounds determined."""

    corrected_paths = []
    for path in paths:
        corrected_path = []
        for x, y in path:
            x -= xmin
            y -= ymin
            corrected_path.append((x, y))
        corrected_paths.append(corrected_path)
    return corrected_paths


def add_path_to_map(path: Path, map: Map) -> None:
    """Adds the given path to the map."""

    for i in range(len(path) - 1):

        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        # Vertical line
        if x1 == x2:
            for _ in range(min(y1, y2), max(y1, y2) + 1):
                map[_][x1] = ROCK

        # Horizontal line
        else:
            for _ in range(min(x1, x2), max(x1, x2) + 1):
                map[y1][_] = ROCK


def create_map(paths: list[Path], x_dim: int, y_dim: int, sand_source: Coordinates) -> Map:
    """Creates a map initialized with the paths."""

    # Create empty map
    map = [[AIR for _ in range(x_dim + 1)] for _ in range(y_dim + 1)]
    sand_x, sand_y = sand_source
    map[sand_y][sand_x] = FALLING_SAND

    # Add paths
    for path in paths:
        add_path_to_map(path, map)

    return map


def print_map(map: Map) -> None:
    """Prints the map to the console."""

    for row in map:
        for cell in row:
            print(cell, end="")
        print()


def move_frame(sand_location: Coordinates, map: Map) -> tuple[bool, Coordinates]:
    """
    Returns True once the sand granule comes to rest, False otherwise, along with the current location of the sand
    granule.
    """

    x, y = sand_location

    if map[y + 1][x] == AIR:
        return False, (x, y + 1)

    if map[y + 1][x - 1] == AIR:
        return False, (x - 1, y + 1)

    if map[y + 1][x + 1] == AIR:
        return False, (x + 1, y + 1)

    return True, (x, y)


def simulate(sand_source: Coordinates, map: Map) -> int:
    """Returns the number of units of sand that come to a rest before sand goes into the abyss."""

    sand_grains = 0
    while True:  # Game loop
        grain_rested = False
        start = sand_source

        # Continue with a grain of sand until it stops moving
        while not grain_rested:
            try:
                grain_rested, start = move_frame(start, map)
            except IndexError:  # Catch grains flowing into the abyss (out of bounds)
                return sand_grains

        if start == sand_source:
            return sand_grains + 1

        # Update map
        map[start[1]][start[0]] = RESTING_SAND
        sand_grains += 1  # One more for every piece of sand that comes to rest


# Main
def main():

    # Record the boundaries of the map
    bounding_coordinates: dict[str, int] = {
        "max_x": 0,
        "max_y": 0,
        "min_x": 500,  # Minimum values from sand coordinates
        "min_y": 0,
    }

    # Load input
    paths: list[Path] = []
    with open("input.txt", 'r') as file:
        for line in file:
            paths.append(path_from_line(line, bounding_coordinates))

    # Part 1

    bounding_coordinates["max_y"] += 2  # Increase Y by two for the sake of part 2
    # Increase the max Y so that there is space for sand to build up
    bounding_coordinates["max_x"] += round((bounding_coordinates["max_x"] - bounding_coordinates["min_x"]) * 5.5)

    # Correct paths using the bounds
    paths = correct_paths(paths, bounding_coordinates["min_x"], bounding_coordinates["min_y"])
    x_dimension = bounding_coordinates["max_x"] - bounding_coordinates["min_x"]
    y_dimension = bounding_coordinates["max_y"] - bounding_coordinates["min_y"]
    corrected_sand = SAND_SOURCE[0] - bounding_coordinates["min_x"], SAND_SOURCE[1] - bounding_coordinates["min_y"]

    # Create map
    map = create_map(paths, x_dimension, y_dimension, corrected_sand)

    # Simulate
    grains = simulate(corrected_sand, map)
    print(f"There are {grains} grains of sand that come to rest before flowing into the abyss.")

    # Part 2

    # Include infinite line
    paths.append([(0, y_dimension), (x_dimension, y_dimension)])

    # Reset the map
    map = create_map(paths, x_dimension, y_dimension, corrected_sand)
    grains = simulate(corrected_sand, map)
    print(f"There are {grains} grains of sand before the source is blocked.")


if __name__ == "__main__":
    main()
