# Advent of Code: Day 16
__author__ = "Matteo Golin"

# Imports
import re
from typing import Self, TypeAlias
from dataclasses import dataclass

# Constants
TIME_LIMIT: int = 30
START_VALVE: str = "AA"


# Utilities
@dataclass
class Valve:
    name: str
    flow: int
    opened: bool = False

    @classmethod
    def from_line(cls, line: str) -> Self:
        """Returns a Valve object made from a line of puzzle input."""
        name = re.findall(r"[A-Z]{2}", line)[0]
        flow_rate = re.search(r"\d+", line)
        flow_rate = int(flow_rate.group(0)) if flow_rate is not None else 0
        return cls(name, flow_rate)

    def open(self) -> None:
        """Open the valve."""
        self.opened = True


ValveSystem: TypeAlias = dict[str, list[Valve]]


class Walker:
    """Moves through the tunnel system to find the best path."""

    def __init__(self, time_limit: int, graph: ValveSystem, start_pos: str) -> None:
        self.time_remaining: int = time_limit
        self.graph: ValveSystem = graph
        self.pos: str = start_pos
        self.pressure: dict[str, int] = {}

    def finished(self) -> bool:
        return self.time_remaining <= 0

    def move(self) -> None:
        """Take a step through the valve system."""

        print(self.pos, self.pressure.get(self.pos))

        if self.time_remaining == 0:
            raise StopIteration("Time out!")

        # Explore paths with highest flow rate
        options = self.graph[self.pos]
        for valve in options:
            # Opening would take too much time
            if not valve.opened and self.time_remaining - 2 < 0:
                break

            # Take the highest flow rate option that is not already opened
            if not valve.opened and valve.flow > 0:
                self.pos = valve.name
                valve.open()  # Open the valve
                self.time_remaining -= 2  # Decrease time taken to move to valve and open it
                self.pressure[valve.name] = valve.flow * self.time_remaining  # Record points from when valve is open
                return

        # No valves were closed
        for valve in options:
            if not valve.opened:
                self.time_remaining -= 1
                self.pos = valve.name
                return

    def pressure_released(self) -> int:
        """Returns the total pressure released so far."""
        return sum(self.pressure.values())


# Main
if __name__ == "__main__":
    # Parse input
    with open("./example.txt", "r") as file:
        # Create valves
        valves: dict[str, Valve] = {}
        for line in file:
            valve = Valve.from_line(line)
            valves[valve.name] = valve

        # Create graph
        file.seek(0)
        graph: ValveSystem = {}
        for line in file:
            connections = re.findall(r"[A-Z]{2}", line)
            graph[connections[0]] = [valves[con] for con in connections[1:]]
            graph[connections[0]].sort(key=lambda x: x.flow, reverse=True)  # Sort from highest to lowest flow

    # Part 1: Most pressure released
    # All valves are equidistant and require 1 minute to travel between
    # All valves take one minute to open
    # Pressure is calculated by multiplying flow rate by time open

    walker = Walker(TIME_LIMIT, graph, START_VALVE)
    while not walker.finished():
        walker.move()

    print(f"The most pressure that can be released in {TIME_LIMIT} minutes is {walker.pressure_released()}")
