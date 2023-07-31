# Advent of Code: Day 15
__author__ = "Matteo Golin"

# Imports
from typing import TypeAlias
from dataclasses import dataclass
import re

# Constants
Coordinates: TypeAlias = tuple[int, int]
Y: int = 2_000_000
LIMIT: int = 4_000_000


def manhattan_distance(sensor: Coordinates, beacon: Coordinates) -> int:
    """Returns the Manhattan distance between two integer coordinates."""
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])


@dataclass
class Sensor:
    x: int
    y: int
    radius: int

    def distance_from(self, coords: Coordinates) -> int:
        """Returns Manhattan distance between sensor and coordinates."""
        return manhattan_distance((self.x, self.y), coords)


def parse_sensor_and_beacon_coordinates(file_line: str) -> tuple[Sensor, Coordinates]:
    """Returns a line of the input file parsed into sensor and beacon coordinates."""
    sx, sy, bx, by = list(map(int, re.findall(r"-?\d+", file_line)))
    beacon = (bx, by)
    return Sensor(sx, sy, manhattan_distance((sx, sy), beacon)), beacon


def row_coverage(y: int, sensors: list[Sensor], minx: int) -> list[bool]:
    """Returns a list which describes which cells in the provided row are within a sensor's coverage zone."""
    row = [False for _ in range(minx, maxx)]
    for sensor in sensors:
        # Skip sensor if radius does not reach row
        higher = sensor.y > y
        extreme = sensor.y - sensor.radius if higher else sensor.y + sensor.radius
        within_range = extreme <= y if higher else extreme >= y
        if not within_range:
            continue

        # Sensor is within range, how many x coordinates are covered
        dist = abs(extreme - y)
        for x in range(dist + 1):
            row[(sensor.x + x) - minx] = True
            row[(sensor.x - x) - minx] = True

    return row


def coverage_ranges(sensors: list[Sensor], limit: int) -> list[list[tuple[int, int]]]:
    """Returns a list where indexes are y coordinates and values are a list of x coordinate ranges that are covered."""
    coverage = [[] for _ in range(limit + 1)]
    for sensor in sensors:
        for height in range(sensor.radius + 1):
            up = sensor.y + height
            down = sensor.y - height
            remaining = sensor.radius - height
            if 0 <= up <= limit:
                coverage[up].append((max(0, sensor.x - remaining), min(limit, sensor.x + remaining)))
            if 0 <= down <= limit:
                coverage[down].append((max(0, sensor.x - remaining), min(limit, sensor.x + remaining)))
    return coverage


def collapse_ranges(ranges: list[tuple[int, int]]) -> tuple[int, int] | int:
    """Returns the collapsed range if collapsible, otherwise returns the value where collapsing failed."""
    ranges.sort(key=lambda x: x[0])
    maxx = ranges[0][1]
    for _ in range(1, len(ranges)):
        if not ranges[0][0] <= ranges[_][0] <= maxx:
            return ranges[_ - 1][1] + 1
        maxx = max(ranges[_][1], maxx)
    return ranges[0][0], maxx


if __name__ == "__main__":
    # Parse input
    sensors: list[Sensor] = []
    beacons: set[Coordinates] = set()
    with open("./input.txt", "r") as file:
        for line in file:
            sensor, beacon = parse_sensor_and_beacon_coordinates(line)
            sensors.append(sensor)
            beacons.add(beacon)

    # Part 1: How many positions cannot contain a beacon in row y=2_000_000

    # Define x limits
    minx, maxx = sensors[0].x, sensors[0].x
    for sensor in sensors[1:]:
        left = sensor.x - sensor.radius
        right = sensor.x + sensor.radius
        if left < minx:
            minx = left
        if right > maxx:
            maxx = right

    # Count coverage in specific row
    row = row_coverage(Y, sensors, minx)

    # Remove beacons
    for beacon in beacons:
        if beacon[1] == Y:
            row[beacon[0] - minx] = False

    print(f"There are {sum(row)} spaces which cannot contain a beacon in row y={Y}.")

    # Part 2: Tuning frequency of distress beacon
    tuning_freq = 0
    ranges = coverage_ranges(sensors, LIMIT)
    for y, range_collection in enumerate(ranges):
        result = collapse_ranges(range_collection)
        if type(result) is int:
            tuning_freq = result * 4_000_000 + y
            break

    print(f"The tuning frequency of the distress beacon is {tuning_freq}")
