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


Tunnel: TypeAlias = tuple[Valve, int]
ValveSystem: TypeAlias = dict[str, list[Tunnel]]


def collapse(graph: ValveSystem, valves: dict[str, Valve], start: str) -> None:
    """Collapse the graph to remove unnecessary 0 flow nodes. Does not remove start position."""

    for valve in valves.values():
        # Don't collapse non-zero flow or start pos
        if valve.flow != 0 or valve.name == start:
            continue

        tunnels = graph[valve.name]
        for v, cost in tunnels:
            tunnels_except_self = [(v, c + cost) for v, c in filter(lambda x: x[0].name != v.name, tunnels)]
            graph[v.name] = list(filter(lambda x: x[0].name != valve.name, graph[v.name]))
            graph[v.name].extend(tunnels_except_self)
        del graph[valve.name]


# Main
if __name__ == "__main__":
    # Parse input
    valves: dict[str, Valve] = {}
    graph: ValveSystem = {}
    with open("./example.txt", "r") as file:
        for line in file:
            valve = Valve.from_line(line)
            valves[valve.name] = valve

        # Create graph
        file.seek(0)
        for line in file:
            connections = re.findall(r"[A-Z]{2}", line)
            graph[connections[0]] = [(valves[con], 1) for con in connections[1:]]  # All tunnels have a cost of 1

    # Collapse graph
    # Valves with flow rate of 0 are useless to open, so they should be condensed into one path leading to a valve with
    # a flow rate > 0.
    collapse(graph, valves, START_VALVE)

    # Part 1: Most pressure released
    # All valves are equidistant and require 1 minute to travel between
    # All valves take one minute to open
    # Pressure is calculated by multiplying flow rate by time open

    print(f"The most pressure that can be released in {TIME_LIMIT} minutes is {0}")
