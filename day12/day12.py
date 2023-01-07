# Advent of Code: Day 12
__author__ = "Matteo Golin"

# Imports
import string

# Constants
Map = list[list[str]]
Coordinates = tuple[int, int]
GraphMap = dict[Coordinates, list[Coordinates]]
Path = list[Coordinates]
ELEVATIONS = list(string.ascii_lowercase)
SURROUNDING: dict[Coordinates, str] = {
    (0, 1): "^",  # Right
    (0, -1): "v",  # Left
    (1, 0): "<",  # Down
    (-1, 0): ">"  # Up
}

START_MARKER = (-1, -1)
END_MARKER = (-2, -2)


# Main
def add_points(point1: Coordinates, point2: Coordinates) -> Coordinates:

    """Returns the sum of two coordinates."""

    x1, y1 = point1
    x2, y2 = point2

    return x1 + x2, y1 + y2


def subtract_points(point1: Coordinates, point2: Coordinates) -> Coordinates:

    """Returns the difference between point1 and point2."""

    x1, y1 = point1
    x2, y2 = point2

    return x1 - x2, y1 - y2


def elevation_of(char_elevation: str) -> int:

    """Returns the integer representation of the elevation."""

    match char_elevation:
        case "S":
            return 0
        case "E":
            return 25
        case _:
            return ELEVATIONS.index(char_elevation)


def valid_neighbours_of(cell: Coordinates, height_map: Map) -> list[tuple[Coordinates, int]]:

    """Returns the list of valid neighbours to the cell (not out of bounds)."""

    valid = []
    for surrounding in SURROUNDING.keys():
        neighbour = add_points(cell, surrounding)

        if -1 not in neighbour:
            try:
                x, y = neighbour
                elevation = elevation_of(height_map[y][x])
                valid.append((neighbour, elevation))
            except IndexError:
                continue

    return valid


def traversable_neighbours_of(cell: Coordinates, height_map: Map) -> list[Coordinates]:

    """Returns a list of all neighbouring cells that can be traversed from the current cell."""

    traversable: list[Coordinates] = []

    # Get the cell's elevation
    x, y = cell
    char_elevation = height_map[y][x]
    elevation = elevation_of(char_elevation)

    # Get the cell's neighbours within bounds of the map
    valid_neighbours = valid_neighbours_of(cell, height_map=height_map)

    for neighbour in valid_neighbours:

        n_pos, n_elevation = neighbour  # Unpack into position and elevation

        # Elevation is one higher or less
        if n_elevation <= elevation + 1:
            traversable.append(n_pos)

    return traversable


def graphify(height_map: Map) -> GraphMap:

    """Turns the input map into a traversable graph."""

    graph = {}

    # Traverse each cell in the map and determine which of its neighbours can be accessed from it
    for y in range(len(height_map)):
        for x in range(len(height_map[0])):

            cell = x, y

            # Add a special marker for the start and end
            if height_map[y][x] == "S":
                graph[START_MARKER] = [cell]
            elif height_map[y][x] == "E":
                graph[END_MARKER] = [cell]

            # Get the neighbours of the cell
            neighbours = traversable_neighbours_of(cell, height_map=height_map)
            graph[cell] = neighbours

    return graph


def traverse_map(graph_map: GraphMap, start: Coordinates) -> Path | None:

    """
    Uses breadth-first search to return the shortest path through the map. If there is no path from the start node
    to the end node, None is returned.
    """

    # Track visited nodes and nodes to be visited
    queue: list[Coordinates] = [start]
    visited: dict[Coordinates, bool] = {start: True}

    # Track parent nodes
    parent: dict[Coordinates, Coordinates] = {}

    while queue:

        # Loop through all neighbours of current node
        node = queue.pop(0)

        for neighbour in graph_map[node]:
            if visited.get(neighbour) is None:
                queue.append(neighbour)  # Mark neighbour to be explored
                visited[neighbour] = True  # Mark neighbour as visited
                parent[neighbour] = node  # Record the neighbour's parent as node

    # It's possible that the end is never reached from the start
    end = graph_map[END_MARKER][0]
    if parent.get(end) is None:
        return None

    # Reconstruct the path from the end to the start
    path: Path = []
    current = end

    # Continue to loop until start is found
    while current != start:
        path.append(current)
        current = parent[current]

    return path


def display_path(path: Path, height_map: Map, start: Coordinates, end: Coordinates) -> None:

    """Prints the path that was taken through the map."""

    # Create display map
    rows = len(height_map)
    cols = len(height_map[0])
    display_map = [["." for _ in range(cols)] for _ in range(rows)]

    # Mark path
    previous_step = path[0]
    for step in path[1:]:

        x, y = step

        # Determine the direction
        direction = subtract_points(step, previous_step)

        # Display the direction
        direction_char = SURROUNDING[direction]
        display_map[y][x] = direction_char

        # Set previous step
        previous_step = step

    # Mark start and end
    display_map[start[1]][start[0]] = "S"
    display_map[end[1]][end[0]] = "E"

    # Show the map
    for row in display_map:
        for cell in row:
            print(cell, end="")
        print()


def main():

    # Load input
    height_map: Map = []
    move_matrix: Map = []
    with open("input.txt", 'r') as file:
        for line in file:
            line = line[:-1]  # Remove newline character
            height_map.append(list(line))
            move_matrix.append(["." for _ in line])

    # Turn the input into a graph
    graph_map: GraphMap = graphify(height_map)
    start: Coordinates = graph_map[START_MARKER][0]
    end: Coordinates = graph_map[END_MARKER][0]

    # Part 1
    # What is the fewest steps required to move from your current position to the best signal location

    # Navigate the map
    path = traverse_map(graph_map, start)

    # Display the path that was used
    display_path(
        path=path,
        height_map=height_map,
        start=start,
        end=end
    )

    print(f"The fewest number of steps required to traverse the map is {len(path)}.")

    # Part two
    # What is the fewest steps required to move starting from any square with elevation a to E

    # Find all starting positions with elevation a
    possible_starts = [start]
    for y in range(len(height_map)):
        for x in range(len(height_map[0])):
            if height_map[y][x] == "a":
                possible_starts.append((x, y))

    # Perform search from all a's
    paths: list[tuple[Coordinates, Path]] = []
    for possible_start in possible_starts:
        path = traverse_map(graph_map, possible_start)
        # Ensure path exists before recording it
        if path is not None:
            paths.append(
                (possible_start, path)
            )

    # Determine the shortest path
    shortest = min(paths, key=lambda p: len(p[1]))
    shortest_path: Path = shortest[1]
    shortest_start: Coordinates = shortest[0]

    # Print shortest path
    display_path(
        path=shortest_path,
        start=shortest_start,
        end=end,
        height_map=height_map
    )

    print(f"The fewest steps required to reach endpoint {end} from the best starting point {shortest_start} is "
          f"{len(shortest_path)}")


if __name__ == '__main__':
    main()
